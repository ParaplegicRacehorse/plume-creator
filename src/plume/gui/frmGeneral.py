import sys
sys.path.insert(0, '../../')
from MuForm import *
from MuCombo import *

class frmGeneral(MuForm):
    def setup(self):
        self.resize(600, 400)
        self.set_title('General Settings')

    def head(self):
        s_html = """
        <script type="text/javascript">
        </script>
        <style type="text/css">

        </style>
        """
        return s_html

    def body(self):
        s_html = self.load_html('form/frmGeneral.html')
        return s_html

    def cssfile(self):
        return 'style/settings.css'

    def nnn(self):
        x = """
        self.read_setting('MainWindow/lang','en_US')
        self.read_setting('MainWindow/style','gtk')
        self.read_setting('MainWindow/displayMode','desktop')
        self.read_setting('Settings/autosaveTime','10000')
        self.read_setting('Updater/checkAtStartup_2','2')
        self.read_setting('Settings/preventDoubleSpace','true')
        self.read_setting('Settings/oneTabOnly','false')
        self.read_setting('Settings/TextArea/noTab','false')
        self.read_setting('MainWindow/isToolBarInStatusBar','true')
        self.read_setting('Settings/numberSymbolIsComma','false')
        """

    def mev_callback_1(self, s_param_1, s_param_2):
        base_info(30301, 'Event!')

    def mev_refresh(self, s_param_1, s_param_2, result=str):
        print('general refresh')
        return self.get_html()

    def mfn_cbo_lang(self):
        a_cbo = MuCombo()
        a_cbo.s_name = 'MainWindow/lang'
        a_cbo.add_option(('en_US', 'English (US)', True))
        a_cbo.add_option(('en_FR', 'French', True))
        a_cbo.add_option(('en_ES', 'Español (España)', True))
        a_cbo.add_option(('en_IT', 'Italiano', True))
        s_html = a_cbo.html()
        return s_html
