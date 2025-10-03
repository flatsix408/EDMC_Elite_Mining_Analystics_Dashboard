const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  readJsonFolder: (folder) => ipcRenderer.invoke('read-json-folder', folder)
});