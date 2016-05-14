'''
Created on April 23th 2016

@author:  Cyril Jacquet
'''

from PyQt5.QtCore import QObject, pyqtSignal, QThread

class TaskManager(QObject):

    # task_state_changed signal : task number, state_code, message
    task_state_changed = pyqtSignal(int, int, 'QString', name='task_state_changed')

    def __init__(self, parent):
        super(TaskManager, self).__init__(parent)
        self._task_list = []

# create permanent database I/O thread:

    def add_task(self, task=QThread):
        pass

    def kill_task(self, id=int):
        pass

    def task_by_id(self, id=int):
        pass


class Task:

    def __init__(self):
        pass


