console.log('Global keys:', Object.keys(global).filter(k => k.toLowerCase().includes('electron') || k.toLowerCase().includes('app')));
console.log('Electron in global:', (global as any).electron ? 'Yes' : 'No');

const { builtinModules } = require('module');
for (const m of builtinModules) {
    try {
        const mod = require(m);
        if (mod && (mod.app || mod.BrowserWindow)) {
            console.log(`FOUND ELECTRON API IN MODULE: ${m}`);
        }
    } catch (e) { }
}

const electron = require('electron');
const path = require('path');
console.log('Electron keys:', Object.keys(electron));
if (typeof electron === 'string') {
    console.log('Electron is a string (path):', electron);
}

const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const ipcMain = electron.ipcMain;

if (!app) {
    console.error("CRITICAL: 'app' is undefined.");
    // Try to fall back or see if it's nested
    if (electron.default && electron.default.app) {
        console.log("Found app in electron.default");
    }
}

app?.whenReady().then(() => {
    console.log("App is ready");
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        }
    });
    win.loadURL('http://localhost:3000');
    win.once('ready-to-show', () => win.show());
});

app?.on('window-all-closed', () => {
    app.quit();
});
