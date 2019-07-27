// Main electron entrance point
// A connection to the Flask server through the main window is created
// in the localhost:5000 port (that can be changed on amphitrite.py) 

const {
    app,
    BrowserWindow,
} = require('electron')

function createWindow() {
    win = new BrowserWindow({show: false})
    win.maximize()
    win.setResizable(false)
    win.show()
    win.setMenu(null)
    win.loadURL('http://127.0.0.1:5000/')
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    // OSX doesn't close the app when the users quit the window
    if (process.platform !== 'darwin') {
        app.quit()
    }
})
