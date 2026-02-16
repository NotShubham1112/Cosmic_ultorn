import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';

const isDev = process.env.NODE_ENV === 'development';

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        show: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
    });

    const url = isDev
        ? 'http://localhost:3000'
        : `file://${path.join(__dirname, '../app/out/index.html')}`;

    mainWindow.loadURL(url);

    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        if (isDev) mainWindow.webContents.openDevTools();
    });
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

// IPC Communication
ipcMain.handle('ping', () => 'pong');
