import ui_converter
import qrc_converter
import constants
from PyQt5.Qt import QApplication
from core.core import Core
from data.database import Database


def launch_gui(core):
    from gui import gui
    gui = gui.Gui(core)
    gui.init_gui()

    return gui


from PyQt5.Qt import QApplication
from core.core import Core
from data.database import Database


def launch_gui(core):
    from gui import gui
    gui = gui.Gui(core)
    gui.init_gui()

    return gui


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    
    app.setApplicationVersion(constants.__version__)
    
    app.setOrganizationName( "Plume-Creator" )
    app.setOrganizationDomain( "plume-creator.eu" )
    app.setApplicationName( "Plume-Creator")
    
    
    
    app.setApplicationVersion(constants.__version__)
    
    app.setOrganizationName( "Plume-Creator" )
    app.setOrganizationDomain( "plume-creator.eu" )
    app.setApplicationName( "Plume-Creator")
    
    
    data = Database(app)
    core = Core(app, data)

    gui = launch_gui(core)

    sys.exit(app.exec_())
