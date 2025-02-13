const { app, BrowserWindow, ipcMain } = require('electron/main')
const path = require('node:path')
const chroma = require('./chroma.js')

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });

    win.loadFile('index.html')
}

app.whenReady().then(() => {
    chroma.initChroma().then((collection) => {
        ipcMain.handle('query', () => {
            console.log('Querying (main)...');
            const response = chroma.db_query(collection, "orange", 3);
            return response;
        })
    });

    ipcMain.handle('ping', () => 'pong')
    createWindow()
})

// Create window when app is activated and no windows are open. (macOS)
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})

// Quit when all windows are closed, except on macOS.
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})