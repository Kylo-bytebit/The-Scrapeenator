const { app, BrowserWindow,ipcMain } = require('electron');
const { exec } = require('child_process');

let flaskProcess;

function createWindow() {
     win = new BrowserWindow({
        width: 800,
        height: 600,
        frame: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadURL('http://127.0.0.1:5000'); // Load Flask Server
    win.setMenuBarVisibility(false);
    win.on('closed', () => {
        win = null;
        if (flaskProcess) flaskProcess.kill(); // Stop Flask when Electron closes
    });
}

app.whenReady().then(() => {
    flaskProcess = exec('python ../backend/ScrapeeNator.py', (err, stdout, stderr) => {
        if (err) {
            console.error(`Flask Error: ${err}`);
        }
        console.log(stdout);
    });

    createWindow();
});

let maximizeToggle=false; // toggle back to original window size if maximize is clicked again
ipcMain.on("manualMinimize", () => {
  win.minimize();
});
ipcMain.on("manualMaximize", () => {
  if (maximizeToggle) {
    win.unmaximize();
  } else {
    win.maximize();
  }
  maximizeToggle=!maximizeToggle; // flip the value of maximizeToggle
});
ipcMain.on("manualClose", () => {
  app.quit();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
