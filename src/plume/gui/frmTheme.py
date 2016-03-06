import sys
sys.path.insert(0, '../../')
from MuForm import *


class frmTheme(MuForm):
    def setup(self):
        self.resize(600, 400)
        self.move(500, 1100)
        self.set_title('Html Form2')

    def head(self):
        s_html = """
        <script type="text/javascript">
        function mNewColor(aInput) {
            alert(aInput.value);
        };

        function mTest() {
            //alert('Go');
            var s_html = MuEv.web_event('refresh', '', '');
            document.open()
            document.write(s_html)
            document.close()
        }
        </script>
        <style type="text/css">

        </style>
        """
        return s_html

    def body(self):
        s_html = self.load_html('form/frmTheme.html')
        return s_html

    def cssfile(self):
        return 'style/settings.css'

    def mev_callback_1(self, s_param_1, s_param_2):
        base_info(30301, 'Event!')

    def mev_refresh(self, s_param_1, s_param_2, result=str):
        return self.get_html()
