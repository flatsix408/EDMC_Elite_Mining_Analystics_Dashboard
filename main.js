const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  win.loadFile('renderer/index.html');
}

ipcMain.handle('select-folder', async () => {
  const result = await dialog.showOpenDialog({ properties: ['openDirectory'] });
  if (result.canceled) return null;
  return result.filePaths[0];
});

ipcMain.handle('read-json-folder', async (event, folderPath) => {
  try {
    const files = fs.readdirSync(folderPath).filter(f => f.endsWith('.json'));
    const sessions = files.map(file => {
      const fullPath = path.join(folderPath, file);
      let data;
      try {
        data = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
      } catch (err) {
        data = null;
      }
      return { file, data };
    }).filter(s => s.data !== null);
    return sessions;
  } catch (err) {
    return [];
  }
});

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });