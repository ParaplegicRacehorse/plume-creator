#
# pl_style - Support for styles settings
# Copyright (C) 2016    Bardi <bardi9@deckertelecom.net>
# Last Error Code: 30703
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


class PlStyleSet:
    #
    # Created by AppSetting, this class holds a collection of defined styles (more precisely, a dict of PlStyle).
    # These styles are also held in the .ini file under key Styles/Style/n.
    #
    def __init__(self, a_setting):  # a_setting is of type AppSetting
        self.a_setting = a_setting
        self.__a_style_dict = {}  # dict of PlStyle
        self.a_top_font_list = []  # List of font-families that we prefer
        # Load does a lot so we don't call it automatically.You should call it after creating your instance

    def set_default_values(self):
        # Called by AppSetting to allow us to generate any default values we want in a blank .ini file.
        a_cfg = self.a_setting.a_config
        self.a_top_font_list = self.set_top_fonts()
        i_count = a_cfg.value('Styles/Style/size', 0)
        # i_count should be zero. However, if there is a partial .ini file, we don't want to destroy existing styles,
        # so we only create a default style if there are no styles
        if i_count == 0:
            # Create a default style
            a_style = PlStyle(self)
            # Create some default values in the style
            a_style.new()
            a_style.s_name = 'Default'
            # Save the style in the ini file (from where we will load it just now in app_settings)
            a_style.save()
            a_cfg.setValue('Styles/Style/size', 1)


    def set_top_fonts(self):
        # These fonts, if they exist on this machine, will appear at the top of font pickers so you don't have to
        # scroll through hundreds of fonts just to find a regular one.
        # The list is also returned
        a_list = ['Times New Roman', 'Arial', 'Courier New', 'Liberation Sans', 'Liberation Serif', 'Apple Garamond',
                  'Geneva']
        self.a_setting.set_value('Styles','TopFonts', a_list)
        return a_list

    def load(self):
        # Loads the list of styles from the .ini file. Most settins (incl the name) can be omitted, but the code
        # is essential to normal operation.
        a_cfg = self.a_setting.a_config

        # Load top (favourite) fonts
        a_cfg.beginGroup('Styles')
        self.a_top_font_list = a_cfg.value('TopFonts', [])
        if len(self.a_top_font_list) == 0:
            self.a_top_font_list = self.set_top_fonts()

        i_count = a_cfg.beginReadArray('Style')

        # Load the styles
        for i_index in range(0, i_count):
            a_cfg.setArrayIndex(i_index)  # Careful: setArrayIndex is zero based, but the .ini file is one-based!
            s_code = a_cfg.value('code', '')
            if s_code == '':
                # We can't continue without this key
                base_error(30704, 'Style {} does not have a code'.format(i_index))
                sys.exit(2)

            # Else, create the style and load
            a_style = PlStyle(self)
            a_style.load(a_cfg, i_index)

            # Add the style to our dict of styles
            self.__a_style_dict[a_style.s_code] = a_style

        a_cfg.endArray()
        a_cfg.endGroup()

    def add_to_set(self, a_style):
        # Stores the style in the set. Any previous style with the same key is discarded
        self.__a_style_dict[a_style.s_code] = a_style

    def next_code(self):
        # Returns a unique style code. For ease of debug, style codes are sxNNN where sx is the string constant 'sx'
        # and NNN is a number > 0. # Do NOT make assumptions about this number. Think of it as 'random'

        # read the settings for all styles to find the highest used code
        a_cfg = self.a_setting.a_config
        a_cfg.beginGroup('Styles')
        i_count = a_cfg.beginReadArray('Style')

        i_max = 0
        for i_index in range(0, i_count):
            a_cfg.setArrayIndex(i_index)
            s_code = a_cfg.value('code', '')
            if s_code[2:]:
                i_code = int(s_code[2:])
            else:
                i_code = 0
            if i_code > i_max:
                i_max = i_code

        a_cfg.endArray()
        a_cfg.endGroup()

        return 'sx' + str(i_max + 1)

    def font_fallback(self):
        # Returns the name of a (hopefully usable) font in this machine. This will be the 'default' font if all else
        # fails. We try the 'TopFonts' in order
        # Get fonts on this machine
        font_db = QFontDatabase()
        a_fonts = font_db.families()

        # Look for the first available top-font
        s_first_font = ''
        for s_font in self.a_top_font_list:
            if not s_first_font:
                s_first_font = s_font  # First font encountered

            if s_font in a_fonts:
                return s_font  # We found a top font. This is our default

        # We didn't find a top font, return the first found font
        if not s_first_font:
            base_error(30701, 'No fonts found')
        else:
            base_info(30702, 'No top font found (see .ini file TopFonts=). Using: ' + s_first_font)

        return s_first_font  # May be '' if no fonts.

    def fonts_available(self):
        # Returns a list of fonts available on this machine. Preferred ('top') fonts are placed at the top of the list
        # as well as at their alphabetic place
        a_ret = []
        # Get fonts on this machine
        font_db = QFontDatabase()

        a_fonts = font_db.families()

        # Add each top font to the return list if it's on this machine
        for s_font in self.a_top_font_list:
            if s_font in a_fonts:
                a_ret.append(s_font)

        # Add rest of available fonts including any already output top fonts
        a_ret += a_fonts

        return a_ret

    def next_index(self):
        # Returns the next available internal style index. (as in a_config.setArrayIndex() )
        a_cfg = self.a_setting.a_config
        a_cfg.beginGroup('Styles')
        i_count = a_cfg.beginReadArray('Style')
        a_cfg.endArray()
        a_cfg.endGroup()

        print('TODO: Test return value')  # TODO: Test return value
        return i_count

    def style(self, s_code):  # -> PlStyle:
        # Returns the style object for the given style code. Returns a new style if s_code = 'new'
        if s_code == 'new':
            # Return a new style
            a_style = PlStyle(self)
            a_style.s_code = self.next_code()

            # Add the style to our dict of styles
            self.__a_style_dict[a_style.s_code] = a_style
            return a_style

        if s_code in self.__a_style_dict:
            # Return an existing style
            return self.__a_style_dict[s_code]

        # Return an empty style to avoid taking a fatal
        a_style = PlStyle(self)
        a_style.s_code = 'new'

    def styles(self):
        # Return dict of styles
        return self.__a_style_dict


#
# pl_style - Support for styles settings
# Copyright (C) 2016    Bardi <bardi9@deckertelecom.net>
# Last Error Code: 30703
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
class PlStyle:
    #
    # A single style
    #
    def __init__(self, a_style_set: PlStyleSet):
        self.__a_style_set = a_style_set
        # Style Code is an internal (str) key for the style. Authoring items should use this code to refer to the style
        # rather than the style name since the user can change the style name at any time. Style Code is guarenteed
        # to be unique across all styles in this project. Apart from that, do not infer anything about its value.
        # After constructing, call either load() or new() to initialise the structure appropriately.
        self.s_code = ''
        self.__i_index = -1  # the index into the settings array for Styles (zero-based)
        self.s_name = 'New'  # Yes, you can have two style with the same name. No, it's not useful to do so.
        self.s_italic = 'N'
        self.s_bold = 'N'
        self.s_font_family = ''
        self.f_font_size = 12.0  # point size (float)
        self.s_fg_color = '#000000'
        self.s_bg_color = ''  # '' = transparent

    def new(self):
        # For a new style, set up some defaults (other simple inits were done at construction)
        self.s_font_family = self.style_set().font_fallback()
        self.s_code = self.style_set().next_code()

    def load(self, a_cfg: QSettings, i_index):
        # For an exisitng style, load the values for this style. a_cfg is set up to the correct index in an array
        # of [Styles]. i_index is passed so we can store it (a_cfg doesn't seem to have a getter for this value...)
        self.__i_index = i_index
        self.s_name = a_cfg.value('name', 'New')
        self.s_code = a_cfg.value('code', '')

        if self.s_code == '':
            # We can't continue without this key
            base_error(30703, 'Style {} does not have a code'.format(i_index))
            sys.exit(2)

        self.s_italic = a_cfg.value('italic', 'N')
        self.s_bold = a_cfg.value('bold', 'N')
        self.s_font_family = a_cfg.value('font-family', '')
        if not self.s_font_family:
            # Get a default font
            base_error(30704, 'Font ' + self.s_name + ' has no font-family')
            self.s_font_family = self.style_set().font_fallback()

        self.f_font_size = float(a_cfg.value('font-size', 12.0))  # point size (float)
        self.s_fg_color = a_cfg.value('color', '#000000')
        self.s_bg_color = a_cfg.value('background-color', '')  # '' = transparent

    def style_set(self):
        # Returns the style list
        return self.__a_style_set

    def font_size(self, f_font_size) -> str:
        # Returns font size as a string with 1 decimal place
        return "{:.1f}".format(float(f_font_size))

    def update_style_set(self):
        # This writes/overwrite the dict entry in the styleSet with this style. If you want to edit a style, you can
        # take a local copy (copy.copy(a_style)) and manipulate it. Then either discard it, or call this function to
        # save it to the list
        self.style_set().add_to_set(self)

    def save(self):
        # Saves the style to the ini file. On entry, a new style will have index = -1.
        # Note if you're operating on a copy of the style, then this is still safe to do, but you probably also want
        # to update the PlStyleSet version of the style (using update_style_set())
        a_cfg = self.style_set().a_setting.a_config

        if self.__i_index == -1:
            # New style
            self.__i_index = self.style_set().next_index()
            # Add to the settings array
            s_key = 'Styles/Style/size'
            a_cfg.setValue(s_key, self.__i_index)

        # Write style info to .ini file
        s_key = 'Styles/Style/' + str(self.__i_index+1)

        a_cfg.beginGroup(s_key)
        # Remove all keys for this style, Only keys we hold will be saved. This is required because some
        # attr e.g. italic, are absent for 'off'.
        a_cfg.remove('')

        # This value is required
        a_cfg.setValue('code', self.s_code)

        a_cfg.setValue('name', self.s_name)
        a_cfg.setValue('font-family', self.s_font_family)
        a_cfg.setValue('font-size', self.font_size(self.f_font_size))
        a_cfg.setValue('color', self.s_fg_color)
        # Only save italic it's used
        if self.s_italic == 'Y':
            a_cfg.setValue('italic', 'Y')
        # Only save bold it's used
        if self.s_bold == 'Y':
            a_cfg.setValue('bold', 'Y')
        # Only save bg if it's not transparent
        if self.s_bg_color != '':
            a_cfg.setValue('background-color', self.s_bg_color)

        a_cfg.endGroup()

    def css(self):
        # Returns a css string suitable for an html style string e.g. <div style="<return-value-of-style_string()>">
        # css example: "font-family:Arial; font-size:12pt; font-style:italic; "
        s_html = ''
        s_html += ('font-family:' + self.s_font_family + '; ')
        s_html += ('font-size:' + self.font_size(self.f_font_size) + 'pt; ')
        s_html += ('color:' + self.s_fg_color + '; ')
        if self.s_bg_color != '':
            s_html += ('background-color:' + self.s_bg_color + '; ')
        s_html += 'font-style:italic; ' if self.s_italic == 'Y' else ''
        s_html += 'font-weight:bold; ' if self.s_bold == 'Y'  else ''

        return s_html
