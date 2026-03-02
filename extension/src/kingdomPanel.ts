import * as vscode from "vscode";
import * as fs from "fs";
import * as path from "path";

export class KingdomPanel {
  public static currentPanel: KingdomPanel | undefined;
  private static readonly viewType = "codeworldKingdom";

  private readonly _panel: vscode.WebviewPanel;
  private readonly _extensionPath: string;
  private _disposed = false;

  public static createOrShow(context: vscode.ExtensionContext) {
    const column = vscode.ViewColumn.Beside;

    // If we already have a panel, show it
    if (KingdomPanel.currentPanel) {
      KingdomPanel.currentPanel._panel.reveal(column);
      return;
    }

    // Create a new panel
    const panel = vscode.window.createWebviewPanel(
      KingdomPanel.viewType,
      "CodeWorld Kingdom",
      column,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
        localResourceRoots: [],
      }
    );

    KingdomPanel.currentPanel = new KingdomPanel(
      panel,
      context.extensionPath
    );
  }

  private constructor(panel: vscode.WebviewPanel, extensionPath: string) {
    this._panel = panel;
    this._extensionPath = extensionPath;

    // Set the webview content
    this._update();

    // Listen for dispose
    this._panel.onDidDispose(() => this.dispose());
  }

  public dispose() {
    KingdomPanel.currentPanel = undefined;
    this._panel.dispose();
    this._disposed = true;
  }

  private _update() {
    const config = vscode.workspace.getConfiguration("codeworld");
    const port = config.get<number>("port", 8765);

    // Try to load webapp/index.html from the codeworld project
    const html = this._getWebviewContent(port);
    this._panel.webview.html = html;
  }

  private _getWebviewContent(port: number): string {
    // Look for webapp/index.html relative to extension
    const candidates = [
      path.join(this._extensionPath, "..", "webapp", "index.html"),
      path.join(this._extensionPath, "webapp", "index.html"),
    ];

    // Also check workspace folders
    const folders = vscode.workspace.workspaceFolders;
    if (folders) {
      for (const folder of folders) {
        candidates.push(
          path.join(folder.uri.fsPath, "webapp", "index.html"),
          path.join(folder.uri.fsPath, "codeworld", "webapp", "index.html")
        );
      }
    }

    for (const candidate of candidates) {
      if (fs.existsSync(candidate)) {
        let html = fs.readFileSync(candidate, "utf-8");

        // Inject CSP meta tag to allow WebSocket connections
        const cspMeta = `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'unsafe-inline'; connect-src ws://localhost:${port} ws://127.0.0.1:${port}; img-src data:;">`;

        // Insert CSP after <head>
        html = html.replace("<head>", "<head>\n" + cspMeta);

        return html;
      }
    }

    // Fallback: minimal page that connects to the server
    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src ws://localhost:${port}; frame-src http://localhost:${port};">
</head>
<body style="margin:0;padding:0;background:#0c1117;overflow:hidden;">
  <iframe src="http://localhost:${port}" style="width:100%;height:100vh;border:none;"></iframe>
</body>
</html>`;
  }
}
