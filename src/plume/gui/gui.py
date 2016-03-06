'''
Created on 3 mars 2015

@author: cyril
'''
from PyQt5.Qt import QObject
from . import cfg, plugins, pics_rc
from .settings import app_setting


class Gui(QObject):

    def __init__(self, core):

        super(Gui, self).__init__()
        cfg.core = core
        # Load settings file
        cfg.a_setting = app_setting.AppSetting()
        cfg.gui_plugins = plugins.Plugins()

    def init_gui(self):

        from .main_window import MainWindow

        self.window = MainWindow(self)
        self.window.show()
        # Bardi for testing only:
        """
        from .form_preference import FormPreference
        a_form = FormPreference()
        a_form.load()
        a_form.show()
        """

