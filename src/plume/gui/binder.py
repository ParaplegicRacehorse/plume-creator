from PyQt5.QtWidgets import QLabel
from .sub_window import SubWindow
from .binder_ui import Ui_Binder


class BinderPanel(SubWindow):

    '''
    classdocs
    '''

    def __init__(self, parent=None, parent_window_system_controller=None):
        '''
        Constructor
        '''
        super(BinderPanel, self).__init__(
            parent=parent, parent_window_system_controller=parent_window_system_controller)
        self.ui = Ui_Binder()
        self.ui.setupUi(self)
        self.setWindowTitle(_("Binder"))
        self.setObjectName("binder_sub_window")

        # label = QLabel("Binder")
        # self.setCentralWidget(label)
