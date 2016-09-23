from PyQt5.QtCore import QObject, QThread, pyqtSlot
from .plugins import Plugins
from .tree.sheet_tree import SheetTree
from .tree.note_tree import NoteTree
from .property.sheet_property_list import SheetPropertyList
from .property.note_property_list import NotePropertyList
from .property.sheet_system_property_list import SheetSystemPropertyList
from .property.note_system_property_list import NoteSystemPropertyList
from .project import Project
from . import cfg, subscriber
from .importer import Importer
import os


class Database(QObject):

    def __init__(self):
        super(Database, self).__init__()
        self.type = None
        self.path = None
        self._project_id = None
        self._sqlite_db = None
        self.subscriber = None
        self._database_id = None
        self.plugins = None

    @pyqtSlot(int, str)
    def init(self, project_id: int, file_name: str):
        self._database_id = project_id
        self._sqlite_db = None
        # init this Database subscriber
        self.subscriber = subscriber.DatabaseSubscriber(self._database_id)
        # loading :
        # TODO adapt to other types :
        if file_name == '':
            self._sqlite_db = Importer.create_empty_sqlite_db()
        else:
            self._sqlite_db = Importer.create_sqlite_db_from("SQLITE", os.path.normpath(file_name))

        self.type = "SQLITE"
        self.path = file_name
        self._project_id = project_id

        # self.subscriber.announce_update("data.project.close")
        self.subscriber.announce_update("database_saved")

        # init all :
        # self.project = Project(self.subscriber, self._sqlite_db)
        # self.sheet_tree = SheetTree(self.subscriber, self._sqlite_db)
        # self.note_tree = NoteTree(self.subscriber, self._sqlite_db)
        self.plugins = Plugins(self.subscriber)

    @pyqtSlot(int)
    def close(self, project_id:int):
        if project_id != self._project_id:
            return

        self._sqlite_db.close()
        self._sqlite_db = None
        self.subscriber.announce_update("database_closed")

    @property
    def sqlite_db(self):
        return self._sqlite_db

    @property
    def sheet_tree(self):
        return SheetTree(self._sqlite_db)

    @property
    def note_tree(self):
        return NoteTree(self._sqlite_db)

    def get_tree(self, table_name: str):
        if table_name == "tbl_sheet":
            return self.sheet_tree
        elif table_name == "tbl_note":
            return self.note_tree

    @property
    def sheet_property_list(self):
        return SheetPropertyList(self._sqlite_db)

    @property
    def note_property_list(self):
        return NotePropertyList(self._sqlite_db)

    @property
    def sheet_system_property_list(self):
        return SheetSystemPropertyList(self._sqlite_db)

    @property
    def note_system_property_list(self):
        return NoteSystemPropertyList(self._sqlite_db)

    def get_table(self, table_name: str):
        if table_name == "tbl_sheet_property":
            return self.sheet_property_list
        elif table_name == "tbl_note_property":
            return self.note_property_list
        elif table_name == "tbl_sheet_system_property":
            return self.sheet_system_property_list
        elif table_name == "tbl_note_system_property":
            return self.note_system_property_list
