import sys
from bin import interfaces
from PyQt4 import QtGui
import platform


def run():
    sys.dont_write_bytecode = True
    if platform.system() is "Windows":  # a quick hack to get app icon show up on taskbar in windows
        import ctypes
        appid = u"pywd"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    app = QtGui.QApplication(sys.argv)  # get the host Qt app
    gui = interfaces.MainWindow()  # get the mainwindow
    gui.app = app  # get main app reference for mainwindow object
    gui.show()  # show the mainwindow
    sys.exit(app.exec_())  # enter app loop


if __name__ == "__main__":
    run()
