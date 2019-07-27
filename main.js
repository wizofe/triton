// Main electron entrance point
// A connection to the Flask server through the main window is created
// in the localhost:5000 port (that can be changed on amphitrite.py) 

const {
    app,
    BrowserWindow
} = require('electron')

function createWindow() {
    window = new BrowserWindow({ width: 1281, height: 800, minWidth: 1281, minHeight: 800 })
    window.loadURL('http://127.0.0.1:5000/')
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})
