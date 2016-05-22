from PyQt5.QtCore import QObject, QUrl, QTimer
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent, QQmlContext
import os, inspect

from . import cfg
from .models.sheet_tree_model import SheetTreeModel
from .models.note_tree_model import NoteTreeModel
from .models.note_list_model import NoteListModel
from plugins.writetreedock.write_tree_proxy_model import WriteTreeProxyModel

class QMLStart(QObject):

    def __init__(self, parent):

        super(QMLStart, self).__init__(parent)

        engine = QQmlApplicationEngine(self)


        cfg.data_subscriber.subscribe_update_func_to_domain(0, self._clear_project,  "database_closed")
        cfg.data_subscriber.subscribe_update_func_to_domain(0, self._activate,  "database_loaded")
        cfg.data.subscriber.subscribe_update_func_to_domain(0, self.set_project_is_saved, "database_saved")

        abspath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.context = engine.rootContext()

        # init Sheet Tree Model
        self.sheet_tree_model = SheetTreeModel(self, 0)
        cfg.models["0_sheet_tree_model"] = self.sheet_tree_model

        # init Sheet Tree Model proxy
        self.sheet_tree_model_filter = WriteTreeProxyModel(self)
        self.sheet_tree_model_filter.setFilterKeyColumn(-1)
        self.sheet_tree_model_filter.setFilterCaseSensitivity(False)
        self.sheet_tree_model_filter.setSourceModel(self.sheet_tree_model)


        self.context.setContextProperty("sheet_tree_model_0", self.sheet_tree_model_filter)
        engine.load(QUrl(abspath + "/qml/main.qml"))


        # init Note Tree Model
        self.note_tree_model = NoteTreeModel(self, 0)
        cfg.models["0_note_tree_model"] = self.note_tree_model
        self.note_list_model = NoteListModel(self, 0)
        cfg.models["0_note_list_model"] = self.note_list_model

        QTimer.singleShot(0, self.init )

    def init(self):



        cfg.data.load_database(0, '../../resources/plume_test_project.sqlite')

        from os.path import expanduser
        home = expanduser("~")
        database = cfg.data.get_database(0)
        database.path = os.path.join(home, "test_project.sqlite")


    def _activate(self, value=True):
        pass

    def _clear_project(self):
        pass

    def set_project_is_saved(self):
        pass
