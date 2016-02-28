#
# MuCombo - support for html combo/dropdown in MuForm
# Copyright (C) 2016    Bardi <bardi9@deckertelecom.net>
# Last Error Code: 30500
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


class MuCombo:
    def __init__(self):
        # Some html defaults:
        self.s_name = 'combo'
        self.s_on_change = ''
        self.a_option = []  # List of tuples (s_key, s_display, b_can_select)
        self.s_selected_value = ''
        self.s_other_attr = ''

    def add_option(self, a_option):
        # Add a tuple option .g. a_option = (s_key, s_display_value, b_can_select)
        # s_key is the 'value' of the <option>
        # s_display_value is the value between the tags <option> and </option>
        # b_can_select if true if this option is still available. Usually true. Example of false: If you sell items
        # and you have a dropdown of colours available and red is no longer available then you cannot simply omit red
        # from the dropdown, because some old orders may contain 'red', and for these orders you want to show that
        # they chose red, but not allow new orders to select red. In this case, set b_can_select to False. when the
        # dropdown is output, red is only included if it is the currently selected value, else it is omitted.
        self.a_option.append(a_option)

    def html(self):
        # Returns the html for a combo The name and id are the name. The option whose value is in s_selected_value
        # is selected. s+other_attr can be used to output any other html into the <select> tag.
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
