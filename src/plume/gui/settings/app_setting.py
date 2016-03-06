#
# app_settings - Support for application settings (.ini) file
# Copyright (C) 2016    Bardi <bardi9@deckertelecom.net>
# Last Error Code: 30600
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFontDatabase
from ..muform.mu_base import *
from .pl_style import *

class AppSetting:
    #
    # This class is a wrapper for the QSettings class. The wrapper provides specific support for plume settings such
    # as styles and fonts, as well as for simple scalar values.
    #
    # This class exposes QSettings (see self.a_config) but developers are recommended not to directly call the QSettings
    # object unless it is essential. More preferable is to modify this class to provide whatever additional
    # functionality is required.
    #

    def __init__(self):
        # Load settings file
        print('Load settings')
        # plume.ini is used for now to avoid conflict with existing plume-creator version
        self.a_config = QSettings('plume.ini', QSettings.IniFormat)
        self.a_config.setFallbacksEnabled(False)

        # Load the styles
        self.__style_set = PlStyleSet(self)

        # Check if an ini file exists, if not, load one
        if self.value('', 'iniVersion', -1) == -1:
            # No ini file detected (or incomplete). Write some default values
            self.set_default_values()

        self.__style_set.load()

    def style_set(self):
        return self.__style_set

    def set_default_values(self):
        # If no .ini file exists, these values are written to a new one:
        self.set_value('', 'iniVersion', 2.0)

        # Let style_set do its own defaults
        self.style_set().set_default_values()

    def value(self, s_group, s_key, a_default = None):
        # Returns the value of s_group/s_key. If s_key is currently undefined, returns the value of a_default.
        if s_group:
            s_key = s_group + '/' + s_key

        return self.a_config.value(s_key, a_default)

    def set_value(self, s_group, s_key, a_value):
        # Sets the value of s_group/s_key.
        if s_group:
            s_key = s_group + '/' + s_key

        return self.a_config.setValue(s_key, a_value)


