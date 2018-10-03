import platform
import sys
from PyQt4 import QtGui
from src import interfaces


def run():
    if platform.system() is "Windows":  # used for making app icon visible in windows taskbar
        import ctypes
        appid = u"pywd2015"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    app = QtGui.QApplication(sys.argv)
    gui = interfaces.MainWindow()
    gui.app = app
    if gui.begin() is 0:
        sys.exit(app.exec_())


if __name__ == "__main__":
    run()
