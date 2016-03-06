#
# form_font_picker - Select font attributes
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
import copy
from .muform.mu_form import *
from .settings.app_setting import *
from . import cfg


class FormFontPicker(MuForm):
    def __init__(self):
        super().__init__()
        self.s_name = 'frmFontPicker'
        self.s_current_form = 'frmFontPicker.html'
        # a_style is a local copy of the style, so we can cancel if we want to
        self.a_style = None  # type: PlStyle
        self.a_attr = {}  # Local copy of Attributes of the current style

    def setup(self):
        self.move(500, 800)
        self.resize(500, 510)
        self.set_title('Select Font')

    def set_style_code(self, s_code):
        # Load style settings. s_code = is the style code or 'new'
        a_setting = cfg.a_setting  # type: AppSetting
        if s_code == 'new':
            self.a_style = PlStyle(a_setting.style_set())
            # Initialise with default font etc
            self.a_style.new()
        else:
            # For existing styles we create a shallow copy of the style so we can cancel if we want to
            self.a_style = copy.copy(a_setting.style_set().style(s_code))

    def head(self):
        s_html = """
        <script type="text/javascript">
        function mSelectFont(sFontName) {
            sHtml = MuEv.web_event('set_font_family', 'font_family', sFontName);
            aDiv = document.getElementById('current_style');
            if (aDiv) {
                aDiv.innerHTML = sHtml;
            }
        }
        """

        # Call the desired setter function for an input that has changed. The return value is used to update the
        # current_style style
        s_html += """
        function mChange(aInp, sSetFunc) {
            sId = aInp.id;
            if (aInp.type == 'checkbox')
                if (aInp.checked)
                    s_value = 'Y';
                else
                    s_value = 'N'
            else
                s_value = aInp.value;
            sHtml = MuEv.web_event(sSetFunc, sId, s_value);
            aDiv = document.getElementById('current_style');
            if (aDiv) {
                aDiv.innerHTML = sHtml;
            }
        }
        """
        # Setter for bg color checkbox
        s_html += """
        function mChangeBg(aInp) {
            // use_bg allows us to NOT pick a background colour (i.e. ~transparent)
            // show/hide bg selector
            aRow = document.getElementById('bg-row');
            if (aInp.checked) {
                aRow.style.visibility = 'visible';
                aBg = document.getElementById('background-color');
                sColour = aBg.value;
            } else {
                aRow.style.visibility = 'hidden';
                sColour = ''; // transparent
            }

            sHtml = MuEv.web_event('set_bg_color', 'bg_color', sColour);
            aDiv = document.getElementById('current_style');
            if (aDiv) {
                aDiv.innerHTML = sHtml;
            }
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
        # Discard any changes to settings.
        from .form_style_picker import FormStylePicker
        a_form = FormStylePicker()
        a_form.load()
        a_form.show()
        self.close()

    def mev_save(self, s_param_1, s_param_2):
        # Save the local style to the style set
        self.a_style.update_style_set()
        # Save to the .ini file
        self.a_style.save()

        # Go back to style picker
        from .form_style_picker import FormStylePicker
        a_form = FormStylePicker()
        a_form.load()
        a_form.show()
        self.close()

    def mfn_style_sample(self):
        # Returns the current font name + a block styled in the current style
        s_html = '<div class="style_sample_font">'
        s_html += self.a_lang.translate('Font:') + ' '
        s_html += self.a_style.s_font_family
        s_html += '</div>'
        s_html += '<div class="style_sample"><div class="label">' + self.a_lang.translate('Sample:') + '</div><div class="inner" style="' + self.a_style.css() + '">' + 'Abc&nbsp;Qzerty' + '</div></div>'
        return s_html

    def mfn_style_font(self):
        # Returns current font name for display only.
        return self.a_style.s_font_family

    def mfn_font_list(self):
        # Outputs an html list of available font names
        a_list = self.a_style.style_set().fonts_available()
        # For each font, output a div with the font name and the font-name styled with that font
        s_html = ''
        i_count = 0
        for s_font in a_list:
            i_count += 1
            s_html += '<div '
            if i_count % 2:
                s_html += 'class="row" '
            else:
                s_html += 'class="row alt" '

            s_html += 'onClick="mSelectFont(\'' + s_font + '\')">'
            s_html += '<div class="font_list_name">' + s_font + '</div>'
            s_html += '<div style="font-family:' + s_font + '">' + s_font + '</div>'
            s_html += '</div>\n'

        return s_html

    #
    # input value setters
    #
    def mev_set_font_family(self, s_id, s_value):
        # Input with id = s_id has changed to s_value
        # A new font is selected
        self.a_style.s_font_family = s_value
        # Return the new sample so the form can update the div
        s_html = self.mfn_style_sample()
        return s_html

    def mev_set_style_name(self, s_id, s_value):
        # Input with id = s_id has changed to s_value
        self.a_style.s_name = s_value
        # Return the new sample so the form can update the div
        s_html = self.mfn_style_sample()
        return s_html

    def mev_set_font_size(self, s_id, s_value):
        # Input with id = s_id has changed to s_value
        self.a_style.f_font_size = s_value
        # Return the new sample so the form can update the div
        s_html = self.mfn_style_sample()
        return s_html

    def mev_set_font_italic(self, s_id, s_value):
        # Input with id = s_id has changed to s_value
        self.a_style.s_italic = s_value
        # Return the new sample so the form can update the div
        s_html = self.mfn_style_sample()
        return s_html

    def mev_set_font_bold(self, s_id, s_value):
        # Input with id = s_id has changed to s_value
        self.a_style.s_bold = s_value
        # Return the new sample so the form can update the div
        s_html = self.mfn_style_sample()
        return s_html

    def mev_set_fg_color(self, s_id, s_value):
        # Input with id = s_id has changed to s_value
        self.a_style.s_fg_color = s_value
        # Return the new sample so the form can update the div
        s_html = self.mfn_style_sample()
        return s_html

    def mev_set_bg_color(self, s_id, s_value):
        # Input with id = s_id has changed to s_value
        self.a_style.s_bg_color = s_value
        # Return the new sample so the form can update the div
        s_html = self.mfn_style_sample()
        return s_html

    #
    # input value getters
    #
    def mfn_style_attr(self):
        # Outputs the rhs list of current font attributes
        s_html = self.load_html(self.form_dir() + 'subFontAttr.html')
        a_parse = MuParse('form_font_picker.mfn.style_attr')
        s_html = a_parse.parse_html(self, s_html)
        return s_html

    def mfn_bg_visible(self):
        # Shows/Hides the bg-row.
        if self.a_style.s_bg_color == '':
            # This style has a transparent background
            return 'visibility:hidden;'
        else:
            # This style has a background colour
            return 'visibility:visible;'

    def mfn_bg_use(self):
        # Returns 'checked' if the background is NOT transparent
        if self.a_style.s_bg_color != '':
            return 'checked'
        return ''

    def mfn_style_name(self):
        # Return style name.
        return self.a_style.s_name

    def mfn_font_size(self):
        # Returns font-size
        return self.a_style.font_size(self.a_style.f_font_size)

    def mfn_font_italic(self):
        if self.a_style.s_italic == 'Y':
            return 'checked'
        return ''

    def mfn_font_bold(self):
        if self.a_style.s_bold == 'Y':
            return 'checked'
        return ''

    def mfn_fg_color(self):
        return self.a_style.s_fg_color

    def mfn_bg_color(self):
        if self.a_style.s_bg_color == '':
            # Transparent.
            return '#e7e7e7'  # Arbitrary color for the picker. e7 is easy to find in the code

        return self.a_style.s_bg_color
