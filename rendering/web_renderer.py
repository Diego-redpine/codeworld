"""WebSocket-based browser renderer for CodeWorld pixel canvas.

Serves an interactive web app that receives binary RGB frames and
JSON scene metadata over WebSocket, with zoom, click-to-inspect,
agent list, stats dashboard, and mobile touch support.
"""
from __future__ import annotations

import asyncio
import logging
import threading
import webbrowser
from pathlib import Path

from websockets.asyncio.server import serve as ws_serve
from websockets.http11 import Response
from websockets import broadcast as ws_broadcast, Headers

log = logging.getLogger(__name__)

# Path to the interactive web app
_WEBAPP_DIR = Path(__file__).resolve().parent.parent / "webapp"

# ═══════════════════════════════════════════════════════════════
# KINGDOM_HTML — self-contained viewer page
# ═══════════════════════════════════════════════════════════════
KINGDOM_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CodeWorld — Red Pine Kingdom</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body {
    width: 100%; height: 100%;
    overflow: hidden;
    background: #0c1117;
  }
  #viewport {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    /* subtle vignette */
    background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.4) 100%);
  }
  canvas {
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    transform-origin: center center;
    border: 2px solid #265c42;
    border-radius: 2px;
    box-shadow: 0 0 40px rgba(38, 92, 66, 0.3), 0 0 80px rgba(0,0,0,0.5);
  }
  #status {
    position: fixed;
    top: 12px; right: 12px;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #e43b44;
    z-index: 10;
    transition: background 0.3s;
    box-shadow: 0 0 6px rgba(228, 59, 68, 0.5);
  }
  #status.connected {
    background: #63c74d;
    box-shadow: 0 0 6px rgba(99, 199, 77, 0.5);
  }
  #title-bar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 32px;
    background: linear-gradient(180deg, rgba(24,20,37,0.95), rgba(24,20,37,0.7));
    display: flex;
    align-items: center;
    padding: 0 16px;
    z-index: 5;
    border-bottom: 1px solid #265c42;
  }
  #title-bar .logo {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: #63c74d;
    letter-spacing: 1px;
  }
  #title-bar .sep {
    color: #3a4466;
    margin: 0 10px;
  }
  #title-bar .subtitle {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: #5a6988;
  }
  #info-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: 24px;
    background: linear-gradient(0deg, rgba(24,20,37,0.95), rgba(24,20,37,0.7));
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    z-index: 5;
    border-top: 1px solid #265c42;
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
  }
  #info-bar span { color: #5a6988; }
  #info-bar .val { color: #feae34; }
  #fps { color: #3e8948; }
</style>
</head>
<body>
<div id="status"></div>
<div id="title-bar">
  <span class="logo">CODEWORLD</span>
  <span class="sep">|</span>
  <span class="subtitle">Red Pine Kingdom</span>
</div>
<div id="viewport">
  <canvas id="screen"></canvas>
</div>
<div id="info-bar">
  <span>RES <span class="val" id="res">--</span></span>
  <span>FPS <span class="val" id="fps">--</span></span>
</div>
<script>
(function() {
  "use strict";

  var canvas = document.getElementById("screen");
  var ctx = canvas.getContext("2d");
  var status = document.getElementById("status");
  var resEl = document.getElementById("res");
  var fpsEl = document.getElementById("fps");
  var frameW = 0, frameH = 0;
  var imageData = null;
  var ws = null;
  var reconnectTimer = null;
  var frameCount = 0;
  var lastFpsUpdate = performance.now();

  function resize() {
    if (frameW === 0 || frameH === 0) return;
    // Reserve space for title and info bars
    var availH = window.innerHeight - 56;
    var availW = window.innerWidth - 24;
    var scaleX = availW / frameW;
    var scaleY = availH / frameH;
    var scale = Math.min(scaleX, scaleY);
    // Snap to integer scale for crispest pixels
    if (scale >= 2) scale = Math.floor(scale);
    canvas.style.transform = "scale(" + scale + ")";
  }

  window.addEventListener("resize", function() {
    requestAnimationFrame(resize);
  });

  function onMessage(evt) {
    if (!(evt.data instanceof ArrayBuffer)) return;
    var view = new DataView(evt.data);
    if (evt.data.byteLength < 4) return;

    var w = view.getUint16(0, false);
    var h = view.getUint16(2, false);
    var expected = 4 + w * h * 3;
    if (evt.data.byteLength < expected) return;

    if (w !== frameW || h !== frameH) {
      frameW = w;
      frameH = h;
      canvas.width = frameW;
      canvas.height = frameH;
      imageData = ctx.createImageData(frameW, frameH);
      resEl.textContent = frameW + "x" + frameH;
      resize();
    }

    var src = new Uint8Array(evt.data, 4);
    var dst = imageData.data;
    var pixels = frameW * frameH;
    for (var i = 0; i < pixels; i++) {
      var si = i * 3;
      var di = i * 4;
      dst[di]     = src[si];
      dst[di + 1] = src[si + 1];
      dst[di + 2] = src[si + 2];
      dst[di + 3] = 255;
    }
    ctx.putImageData(imageData, 0, 0);

    // FPS counter
    frameCount++;
    var now = performance.now();
    if (now - lastFpsUpdate > 1000) {
      fpsEl.textContent = frameCount;
      frameCount = 0;
      lastFpsUpdate = now;
    }
  }

  function connect() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
    ws = new WebSocket("ws://localhost:{{PORT}}");
    ws.binaryType = "arraybuffer";

    ws.onopen = function() {
      status.classList.add("connected");
    };

    ws.onmessage = onMessage;

    ws.onclose = function() {
      status.classList.remove("connected");
      reconnectTimer = setTimeout(connect, 2000);
    };

    ws.onerror = function() {
      ws.close();
    };
  }

  connect();
})();
</script>
</body>
</html>
"""


# ═══════════════════════════════════════════════════════════════
# WebRenderer — asyncio WebSocket server in a daemon thread
# ═══════════════════════════════════════════════════════════════

class WebRenderer:
    """Stream PixelCanvas frames to a browser via WebSocket.

    Usage::

        renderer = WebRenderer(port=8765)
        renderer.start()            # opens browser, starts server thread
        renderer.send_frame(canvas.to_rgb_bytes())
        ...
        renderer.stop()
    """

    def __init__(self, host: str = "localhost", port: int = 8765):
        self._host = host
        self._port = port
        self._connections: set = set()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._latest_frame: bytes | None = None
        # Pre-cache HTML to avoid disk I/O in the asyncio event loop
        self._cached_html: bytes | None = None
        self._sending = False  # Throttle: skip frames while a send is in flight

    # ── public API ────────────────────────────────────────────

    def start(self, open_browser: bool = True):
        """Start the WebSocket server in a daemon thread."""
        self._thread = threading.Thread(
            target=self._run_server,
            name="codeworld-web-renderer",
            daemon=True,
        )
        self._thread.start()

        if open_browser:
            # Give the server a moment to bind
            timer = threading.Timer(
                0.5,
                webbrowser.open,
                args=[f"http://{self._host}:{self._port}"],
            )
            timer.daemon = True
            timer.start()

        log.info(
            "WebRenderer serving on http://%s:%d",
            self._host,
            self._port,
        )

    def send_frame(self, frame_bytes: bytes):
        """Thread-safe: broadcast frame to all connected browsers."""
        self._latest_frame = frame_bytes
        if self._loop and self._connections and not self._sending:
            self._sending = True
            self._loop.call_soon_threadsafe(
                self._loop.create_task,
                self._broadcast(frame_bytes),
            )

    def send_scene(self, manifest: dict):
        """Thread-safe: broadcast scene manifest as JSON text to all browsers."""
        import json
        text = json.dumps(manifest, separators=(',', ':'))
        if self._loop and self._connections:
            self._loop.call_soon_threadsafe(
                self._loop.create_task,
                self._broadcast_text(text),
            )

    async def _broadcast_text(self, text: str):
        """Send text message to all connected WebSocket clients."""
        ws_broadcast(self._connections, text)

    def stop(self):
        """Stop the server and clean up."""
        if self._loop and hasattr(self, '_stop_event'):
            self._loop.call_soon_threadsafe(self._stop_event.set)
        if self._thread:
            self._thread.join(timeout=3)

    # ── internals ─────────────────────────────────────────────

    def _run_server(self):
        """Run the asyncio event loop for the server."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._serve())
        except asyncio.CancelledError:
            pass
        finally:
            self._loop.run_until_complete(self._loop.shutdown_asyncgens())
            self._loop.close()

    async def _serve(self):
        """Start websockets server with process_request hook."""
        self._server = await ws_serve(
            self._ws_handler,
            self._host,
            self._port,
            process_request=self._process_request,
        ).__aenter__()
        self._stop_event = asyncio.Event()
        await self._stop_event.wait()
        self._server.close()
        await self._server.wait_closed()

    async def _process_request(self, connection, request):
        """Serve web app for regular HTTP requests."""
        # If the request has an Upgrade header it is a WebSocket handshake;
        # let the library handle it normally.
        if request.headers.get("Upgrade", "").lower() == "websocket":
            return None

        # Serve the interactive web app (cached in memory)
        if self._cached_html is None:
            webapp_file = _WEBAPP_DIR / "index.html"
            if webapp_file.exists():
                self._cached_html = webapp_file.read_bytes()
            else:
                self._cached_html = KINGDOM_HTML.replace(
                    "{{PORT}}", str(self._port)
                ).encode("utf-8")
        body = self._cached_html

        headers = Headers(
            [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Content-Length", str(len(body))),
                ("Connection", "close"),
            ]
        )
        return Response(200, "OK", headers, body)

    async def _ws_handler(self, websocket):
        """Handle a WebSocket connection."""
        self._connections.add(websocket)
        try:
            # Send the latest frame immediately so the client
            # does not stare at a blank canvas.
            if self._latest_frame:
                await websocket.send(self._latest_frame)
            # Keep connection alive -- just wait for close
            async for _ in websocket:
                pass
        finally:
            self._connections.discard(websocket)

    async def _broadcast(self, data: bytes):
        """Send frame to all connected WebSocket clients."""
        ws_broadcast(self._connections, data)
        self._sending = False
        # Yield to event loop so HTTP requests can be processed
        await asyncio.sleep(0)
