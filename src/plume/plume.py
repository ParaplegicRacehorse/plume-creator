import ui_converter,  qrc_converter,  constants
import qrc_converter
from PyQt5.Qt import QApplication
from core.core import Core
from data.data import Data
import sys


def launch_gui(core):
    from gui import gui
    gui = gui.Gui(core)
    gui.init_gui()

    return gui

if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    app.setApplicationVersion(constants.__version__)
    
    app.setOrganizationName( "Plume-Creator" )
    app.setOrganizationDomain( "plume-creator.eu" )
    app.setApplicationName( "Plume-Creator")
    data = Data()
    
    
    core = Core(app, data)

    gui = launch_gui(core)

    sys.exit(app.exec_())
