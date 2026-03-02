import * as vscode from "vscode";
import { KingdomPanel } from "./kingdomPanel";
import { ChildProcess, spawn } from "child_process";
import * as path from "path";
import * as fs from "fs";
import * as net from "net";

let pythonProcess: ChildProcess | null = null;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
  outputChannel = vscode.window.createOutputChannel("CodeWorld");

  // Register open command
  context.subscriptions.push(
    vscode.commands.registerCommand("codeworld.openKingdom", () => {
      ensureServerRunning(context).then(() => {
        KingdomPanel.createOrShow(context);
      });
    })
  );

  // Register stop command
  context.subscriptions.push(
    vscode.commands.registerCommand("codeworld.stopServer", () => {
      stopPythonProcess();
      vscode.window.showInformationMessage("CodeWorld server stopped.");
    })
  );

  // Auto-start if configured
  const config = vscode.workspace.getConfiguration("codeworld");
  if (config.get<boolean>("autoStart", true)) {
    ensureServerRunning(context).then(() => {
      KingdomPanel.createOrShow(context);
    });
  }
}

export function deactivate() {
  stopPythonProcess();
}

async function ensureServerRunning(
  context: vscode.ExtensionContext
): Promise<void> {
  const config = vscode.workspace.getConfiguration("codeworld");
  const port = config.get<number>("port", 8765);

  // Check if server is already running
  const isRunning = await checkPort(port);
  if (isRunning) {
    outputChannel.appendLine(`Server already running on port ${port}`);
    return;
  }

  // Find the codeworld project root
  const codeworldRoot = findCodeworldRoot(context);
  if (!codeworldRoot) {
    vscode.window.showErrorMessage(
      "CodeWorld: Could not find codeworld project. Open the codeworld folder in VS Code."
    );
    return;
  }

  // Find Python interpreter
  const pythonPath = await findPython(config, codeworldRoot);
  if (!pythonPath) {
    vscode.window.showErrorMessage(
      "CodeWorld: Could not find Python interpreter. Set codeworld.pythonPath in settings."
    );
    return;
  }

  // Build args
  const args = [path.join(codeworldRoot, "main.py"), "--headless"];

  const revenue = config.get<number>("revenue", 0);
  const customers = config.get<number>("customers", 0);
  if (revenue > 0) {
    args.push("--revenue", String(revenue));
  }
  if (customers > 0) {
    args.push("--customers", String(customers));
  }

  outputChannel.appendLine(`Starting: ${pythonPath} ${args.join(" ")}`);

  pythonProcess = spawn(pythonPath, args, {
    cwd: codeworldRoot,
    stdio: ["ignore", "pipe", "pipe"],
  });

  pythonProcess.stdout?.on("data", (data: Buffer) => {
    outputChannel.appendLine(data.toString().trim());
  });

  pythonProcess.stderr?.on("data", (data: Buffer) => {
    outputChannel.appendLine(`[stderr] ${data.toString().trim()}`);
  });

  pythonProcess.on("exit", (code) => {
    outputChannel.appendLine(`Python process exited with code ${code}`);
    pythonProcess = null;
  });

  // Wait for server to be ready
  await waitForPort(port, 10000);
  outputChannel.appendLine(`Server ready on port ${port}`);
}

function findCodeworldRoot(context: vscode.ExtensionContext): string | null {
  // Check if extension is inside the codeworld project
  const extDir = context.extensionPath;
  const parentDir = path.dirname(extDir);
  if (fs.existsSync(path.join(parentDir, "main.py"))) {
    return parentDir;
  }

  // Check workspace folders
  const folders = vscode.workspace.workspaceFolders;
  if (folders) {
    for (const folder of folders) {
      const p = folder.uri.fsPath;
      if (fs.existsSync(path.join(p, "main.py"))) {
        return p;
      }
      // Check if codeworld is a subdirectory
      const sub = path.join(p, "codeworld");
      if (fs.existsSync(path.join(sub, "main.py"))) {
        return sub;
      }
    }
  }

  return null;
}

async function findPython(
  config: vscode.WorkspaceConfiguration,
  codeworldRoot: string
): Promise<string | null> {
  // 1. Check user setting
  const configPath = config.get<string>("pythonPath", "");
  if (configPath && fs.existsSync(configPath)) {
    return configPath;
  }

  // 2. Check venv in codeworld project
  const venvPython = path.join(codeworldRoot, ".venv", "bin", "python3");
  if (fs.existsSync(venvPython)) {
    return venvPython;
  }

  // 3. Check VS Code Python extension's selected interpreter
  const pyExt = vscode.extensions.getExtension("ms-python.python");
  if (pyExt?.isActive) {
    const api = pyExt.exports;
    if (api?.settings?.getExecutionDetails) {
      const details = api.settings.getExecutionDetails(
        vscode.workspace.workspaceFolders?.[0]?.uri
      );
      if (details?.execCommand?.[0]) {
        return details.execCommand[0];
      }
    }
  }

  // 4. Fallback to system python3
  return "python3";
}

function checkPort(port: number): Promise<boolean> {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    socket.setTimeout(1000);
    socket.on("connect", () => {
      socket.destroy();
      resolve(true);
    });
    socket.on("timeout", () => {
      socket.destroy();
      resolve(false);
    });
    socket.on("error", () => {
      resolve(false);
    });
    socket.connect(port, "localhost");
  });
}

function waitForPort(port: number, timeoutMs: number): Promise<void> {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const check = () => {
      checkPort(port).then((ready) => {
        if (ready) {
          resolve();
        } else if (Date.now() - start > timeoutMs) {
          reject(new Error(`Timeout waiting for port ${port}`));
        } else {
          setTimeout(check, 500);
        }
      });
    };
    check();
  });
}

function stopPythonProcess() {
  if (pythonProcess) {
    pythonProcess.kill("SIGTERM");
    pythonProcess = null;
    outputChannel.appendLine("Python process stopped.");
  }
}
