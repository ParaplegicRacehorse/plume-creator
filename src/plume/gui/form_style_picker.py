#
# form_style - Display text style settings
# Copyright (C) 2016    Bardi <bardi9@deckertelecom.net>
# Last Error Code:
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
from .muform.mu_form import *
from .settings.app_setting import *
from . import cfg


class FormStylePicker(MuForm):
    def __init__(self):
        super().__init__()
        self.s_name = 'frmStyle'
        self.s_current_form = 'frmStylePicker.html'
        self.move(500, 800)

    def setup(self):
        self.resize(500, 510)
        self.set_title('Styles')

    def head(self):
        s_html = """
        <script type="text/javascript">
        function mSelectStyle(sStyleName) {
            MuEv.web_event('font_edit', sStyleName, '');
        }
        </script>
        <style type="text/css">
        </style>
        """
        return s_html

    def body(self):
        s_html = self.load_html(self.form_dir() + self.s_current_form)
        return s_html

    def cssfile(self):
        return base_style_dir()  + 'preference.css'

    def mev_cancel(self, s_param_1, s_param_2):
        # Discard any changes to settings
        self.close()

    def mev_close(self, s_param_1, s_param_2):
        # No save, this is just a view
        self.close()

    def mfn_style_list(self):
        # One div per style, formated in that style.
        a_set = cfg.a_setting  # type: AppSetting
        a_dict = a_set.style_set().styles()

        # Create a simple dict to sort.
        # Sort the styles by name.
        a_list = {}
        for s_code in a_dict:
            a_list[s_code] = a_set.style_set().style(s_code).s_name

        # Sort the dict by value (stylename)
        a_list = sorted(a_list, key=a_list.get)

        # Generate html list
        s_html = ''
        i_count = 0
        for s_code in a_list:
            a_style = a_set.style_set().style(s_code)  # type: PlStyle
            i_count += 1
            s_name = a_style.s_name
            s_html += '<div '
            if i_count % 2:
                s_html += 'class="row" '
            else:
                s_html += 'class="row alt" '

            s_html += 'onClick="mSelectStyle(\'' + s_code + '\')">'  # end of outer <div>

            # item div with style name, styled to show how style looks
            s_html += '<div class="item" '
            s_html += 'style="' + a_style.css() + '"'
            s_html += '>' + s_name + '</div>'
            s_html += '</div>\n'  # outer </div>

        return s_html

    def mev_font_edit(self, s_code, s_param_2):
        from .form_font_picker import FormFontPicker
        a_form = FormFontPicker()
        a_form.set_style_code(s_code)
        a_form.load()
        a_form.show()
        self.close()
