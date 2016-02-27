from .muform.mu_form import *
from PyQt5.QtCore import QSettings


class FormPreference(MuForm):
    # Parent form for settings
    def __init__(self):
        super().__init__()
        self.s_form_name = 'frmPreference'
        self.a_config = QSettings('plume.ini', QSettings.IniFormat)
        self.a_config.setFallbacksEnabled(False)
        self.a_config_list = []
        self.s_current_form = 'frmPreference.html'
        self.move(500, 1100)

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

    def read_setting(self, s_key, s_default):
        self.a_config_list[s_key] = self.a_config.value(s_key, s_default)

    def read_config(self):
        # General
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

        # Text
        # Main window font!
        self.read_setting('Settings/NoteArea/textFontFamily','@other@')
        self.read_setting('Settings/NoteArea/textHeight','12')
        self.read_setting('Settings/NoteArea/showScrollbar','true')
        self.read_setting('Settings/NoteArea/textIndent','20')
        self.read_setting('Settings/NoteArea/bottomMargin','10')

        self.read_setting('Settings/SynArea/textFontFamily','@other@')
        self.read_setting('Settings/SynArea/textHeight','12')
        self.read_setting('Settings/SynArea/showScrollbar','true')
        self.read_setting('Settings/SynArea/textIndent','20')
        self.read_setting('Settings/SynArea/bottomMargin','10')

        # Theme
        self.read_setting('Themes/theme','/usr/share/plume-creator/themes/AJstyle.plume_theme')
        self.read_setting('Settings/applyCustomColors','true')
        self.read_setting('MainWindow/textZoneBackColor','#ffffff')
        self.read_setting('MainWindow/textZoneTextColor','#000000')
        self.read_setting('MainWindow/textTabBackColor','#ffffff')
        self.read_setting('MainWindow/projectTreeBackColor','#dee4ea')
        self.read_setting('MainWindow/projectTreeTextColor','#000000')
        self.read_setting('MainWindow/noteZoneBackColor','#fff7d7')
        self.read_setting('MainWindow/noteZoneTextColor','#000000')

        # Styles
        #! Not found!

        # Spelling
        self.read_setting('SpellChecking/lang','en_GB')
        self.read_setting('SpellChecking/includeNamesFromTheMiseEnScene','true')
        #GUI not found:
        # self.read_setting('SpellChecking/globalSpellCheckActivated','true')

        # Proxy
        self.read_setting('Updater/Proxy/proxyEnabled','false')
        self.read_setting('Updater/Proxy/proxySystemEnabled','true')
        self.read_setting('Updater/Proxy/proxyHostName','')
        self.read_setting('Updater/Proxy/proxyPort','1080')
        self.read_setting('Updater/Proxy/proxyUserName','')
        self.read_setting('Updater/Proxy/proxyPassword','')

        #self.read_setting('Updater/Proxy/proxyType','http')
        #self.read_setting('Updater/linuxDistrib','0')

    def x_geT_all_settings(self):
        s_comment = """
        a_all = self.a_config.allKeys()
        for a in a_all:
            s_value = self.a_config.value(a)
            if type(s_value) != str:
                s_value = '@other@'
            print("self.read_setting('" + a + "','" + s_value + "')")
        """

    def body(self):
        s_html = self.load_html(self.form_dir() + self.s_current_form)
        return s_html

    def style(self):
        return base_style_dir()  + 'preference.css'

    def mev_refresh(self, s_param_1, result=str):
        print('config refresh')
        # change size
        self.setup()
        return self.get_html()

    def mev_cancel(self, s_param_1):
        # Discard any changes to settings
        self.close()


    def mev_save(self, s_param_1):
        # Save changes to settings
        #self.a_web
        print('Save')
        self.close()

    def mev_go_general(self, s_param_1):
        # Overload this form with the general settings
        #a_form = frmGeneral('general', self)
        #a_form.load_r()
        #return a_form.get_html()
        print('Loading...')
        self.a_web
        pass


