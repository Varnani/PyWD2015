import platform
import sys
from PyQt4 import QtGui
from bin import interfaces


# TODO add red emphasis on selected keeps and dels
# TODO add tooltips, statustips and whatsthis on every parameter
# TODO add file picker for missing files in loadProject()
# TODO add program input control (mode, ifcgs, maglite/xcalib etc.)
# TODO add dc subset support
# TODO finish implementing saveProject()/loadProject()
# TODO add in/out file archiving
# TODO make windows compatible

def run():
    if platform.system() is "Windows":  # a quick hack to get app icon show up on taskbar in windows
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
