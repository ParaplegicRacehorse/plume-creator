from .muform.mu_form import *
from PyQt5.QtCore import QSettings


class FormPreference(MuForm):
    # Parent form for settings
    def __init__(self):
        super().__init__()
        self.s_name = 'frmPreference'
        self.a_config = QSettings('plume.ini', QSettings.IniFormat)
        self.a_config.setFallbacksEnabled(False)
        self.a_config_list = []
        self.s_current_form = 'frmPreference.html'
        self.move(500, 900)

    def setup(self):
        self.resize(400, 310)
        self.set_title('Settings')

    def head(self):
        s_html = """
        <script type="text/javascript">
        function mAlert()
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

    def mev_close(self, s_param_1, s_param_2):
        # Nothing to save - thi sis a view only
        self.close()

    def mev_show_style(self, s_param_1, s_param_2):
        # Open style window
        from .form_style_picker import FormStylePicker
        a_form = FormStylePicker()
        a_form.load()
        a_form.show()
