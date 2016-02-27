#
# MuCombo - support for html combo
#

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo, pyqtSlot, QObject
from PyQt5 import QtWebKitWidgets
import sys
import os
import datetime
from .mu_base import *
from .mu_parse import *

class MuCombo:
    # Last Error Code: 30500
    def __init__(self):
        # Some html defaults:
        self.s_name = 'combo'
        self.s_on_change = ''
        self.a_option = []  # List of tuples (key, display, b_can_select)
        self.s_selected_value = ''
        self.s_other_attr = ''

    def add_option(self, a_option):
        # Add a tuple. a_option = (key,display-value, can-select)
        self.a_option.append(a_option)

    def html(self):
        # Returns the html for a combo
        s_html = '<select name="' + self.s_name + '" id="' + self.s_name + '"'
        if self.s_on_change:
            s_html += ' onchange="' + self.s_on_change + '"'

        if self.s_other_attr:
            s_html += ' ' + self.s_other_attr

        s_html += '>\n'

        # Add options
        for a_opt in self.a_option:
            s_key = a_opt[0]
            s_display = a_opt[1]
            b_can_select = a_opt[2]

            # Is this option selected?
            if s_key == self.s_selected_value:
                s_html += '<option selected value="' + s_key + '">' + s_display + '</option>\n'
            elif b_can_select:
                s_html += '<option value="' + s_key + '">' + s_display + '</option>\n'
            # Note, a non-selectable option is not output unless it is the selected option. This allows us to display
            # an option that was previously valid and selected, but is no longer valid.

        # Close
        s_html += '</select>\n'

        return s_html



