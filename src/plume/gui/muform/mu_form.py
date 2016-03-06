#
# MuForm - Support for forms using HTML for gui
# Copyright (C) 2016    Bardi <bardi9@deckertelecom.net>
# Last Error Code: 30301
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
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5 import QtWebKitWidgets
import time
import datetime
from .mu_parse import *
from .mu_base import *

class MuLate():
    # Provides multilingual support
    def translate(self, s_source, s_context = ''):
        # s_source is the string to translate
        # s_context is eithe rthe form name ot 'base' for common strings (e.g. 'ok'). It allows the phrase to occur
        # multiple times in the application with different translations. If further disambiguation is required, append
        # further context with . e.g.
        #   translate('open', 'base.file')
        #   translate('open', 'base.connect')
        #
        #TODO: Either use Qt or some other service...
        return '~' + s_source


class MuForm:
    # An MuForm is a python form that uses html for its layout
    # We try and isolate ourselves from Qt since we might in future we able to use the webkit directly.
    def __init__(self):
        # If a_aprent is set (to anothe rMuForm), then this window will use the parent qt window and not create on
        # itself. This is useful for overloading the contents of one window with another (child) window as per the
        # settings where the same qt window is used to display all pages of settings (which allows data sharing too)
        # Some html defaults:
        self.s_url_root = base_root_url()
        self.s_html = '' # Unparsed html
        self.b_dump = False # For debug - see <(dump)>
        self.s_name = 'muForm'  # It's a good idea to give your forms names to help with parsing errors
        self.a_lang = MuLate() # Translation support
        # Declare some publics

        self.a_win = None  # type: QtWebKitWidgets.QWebView
        self.a_web = None
        self.__gui()

        # Call child setup
        self.setup()

    def __gui(self):
        # Create a new window
        self.a_win = QWidget()
        self.a_win.setObjectName("MuForm")

        # Create the webview
        self.a_web = QtWebKitWidgets.QWebView(self.a_win)
        self.a_web.page().mainFrame().documentElement()
        # Create Event handler (for callbacks from webview)
        self.a_event = MuEvent(self)

        # Make the webview resize with the form
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(80)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.a_win.sizePolicy().hasHeightForWidth())
        self.a_win.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.a_win)
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.a_web)

    def setup(self):
        # Subclasses can set title, size, html in here:
        pass

    #
    # These methods manipulate the webview
    #
    def set_url(self, s_url):
        # Display a url in the web view. Note: Without the full command set of a browser (back button, address bar etc),
        # this is of limited usefulness
        self.a_web.setProperty("url", QtCore.QUrl(s_url))

    def set_html(self, s_html):
        # Load a string of html into the webview. The string should contain everything from <html> to </html>
        self.a_web.setContent(s_html, 'text/html', QtCore.QUrl(self.s_url_root))
        pass

    def element_by_selector(self, s_selector):
        # Returns the first element in the web view that matches the given css selector.
        # E.g. element_by_selector('input[id=foo]')
        a_element = self.a_web.page().mainFrame().findFirstElement(s_selector)
        return a_element

    def element_by_id(self, s_id):
        # Returns the first element in the web view that matches the given element id
        # E.g. for <input id="foo"> use: element_by_id('foo')
        a_element = self.element_by_selector("input[id='" + s_id + "']")
        return a_element

    def value_by_id(self, s_id):
        # Returns the value of the first element in the web view that matches the given element id
        # E.g. for <input id="foo"> use: value_by_id('foo')
        # Note: a_element.attribute("value") only returns the ORIGINAL value of the input, Apparently that's a feature.

        a_element = self.element_by_selector("input[id='" + s_id + "']")
        print(a_element.attribute("type"))
        if a_element.attribute("type") == 'checkbox':
            return self.a_web.page().mainFrame().evaluateJavaScript("document.getElementById('" + s_id + "').checked")
        else:
            return self.a_web.page().mainFrame().evaluateJavaScript("document.getElementById('" + s_id + "').value")

    #
    # These methods manipulate the window
    #
    def resize(self, i_x, i_y):
        self.a_win.resize(i_x, i_y)

    def move(self, i_x, i_y):
        self.a_win.move(i_x, i_y)

    def set_title(self, s_title):
        s_title = self.a_lang.translate(s_title)
        self.a_win.setWindowTitle(s_title)

    def show(self):
        self.a_win.show()

    def close(self):
        self.a_win.destroy()
        #del self.a_win
        #del self

    #
    # These methods provide help for loading html strings
    #
    def load(self):
        # Load and parse an entire form. You can call this or do the separate bits yourself, depending on your need
        # Get template html
        self.s_html = ''
        s_template = self.template()
        if s_template:
            self.s_html = self.load_html(s_template)

        # If we have a template, then it should call the body. If no template html, get the body text directly
        if not self.s_html:
            # No template html, get the body directly
            self.s_html = self.body()

        # Now parse the html and output it to the webview. We leave the un-parsed html in self.s_html so we can
        # call refresh again if needed
        self.refresh()
        QApplication.processEvents()  # Allows webView time to display form before we call show()

    def load_r(self):
        # Load and parse an entire form. You can call this or do the separate bits yourself, depending on your need
        # Get template html
        self.s_html = ''
        s_template = self.template()
        if s_template:
            self.s_html = self.load_html(s_template)

        # If we have a template, then it should call the body. If no template html, get the body text directly
        if not self.s_html:
            # No template html, get the body directly
            self.s_html = self.body()

    def refresh(self):
        # Re-parse the html and copy to the webview.
        s_html = self.get_html()

        # Now insert the html into the page
        self.set_html(s_html)

    def get_html(self):
        # Returns the parsed html. s_name is passed so errors contain some context.
        a_parse = MuParse(self.s_name)
        # self.s_html is either the template or if no template, the body.
        s_html = a_parse.parse_html(self, self.s_html)

        # If dump is on, output the html for debug
        if self.b_dump:
            print(s_html)

        return s_html

    def form_dir(self):
        # Returns the subfolder containing forms and templates
        return base_form_dir()

    def load_html(self, s_path):
        # Load the text of a file. We expect them to be html fragments, but we don't care - GIGO
        s_abs_path = base_path(s_path)
        a_file = open(s_abs_path, 'r')
        s_html = a_file.read()
        a_file.close()
        return s_html

    def template(self):
        # Returns the html template path
        return self.form_dir() + 'templateA.html'

    #
    # These methods offer html fragments
    #
    def cssfile(self):
        # Returns the stylesheet path
        return base_style_dir() + 'default.css'

    def head(self):
        # the html to insert in the <head> section e.g. style, javascript
        return ''

    def body(self):
        # The html to output in the <body> section, or if no template, the entire html
        # You will want to overload this function (unless you like Hello World). your body method can either
        # generate html or load it from a file.
        return 'Hello World'

    #
    # These methods offer values to the html via the tag syntax. A MuForm tag is enclosed in <( and )>
    # Examples:
    # A comment:
    #   <(# is a comment )>
    # A function call
    #   <(func, arg1, argn)> - calls the method in this class called mfn_func(arg1, argn)
    #
    # Some generic methods are provided, it is expected that forms will subclass MuForm and provide their own
    # functions.
    # Note: In addition, the following pseudo methods are provided by the parser: <(dump)> <(debug, on)> <(debug, off)>
    #
    def mfn_head(self):
        # Used by a template to insert in the <head> section e.g. style, javascript
        # Usage in html: <(head)>
        return self.head()

    def mfn_cssfile(self):
        # Used by a template to return the stylesheet name
        # Usage in html: <(cssfile)>
        return self.cssfile()

    def mfn_body(self):
        # Used by a template to insert the body
        # Usage in html: <(body)>
        return self.body()

    def mfn_root(self):
        # Returns root folder
        # Usage in html: <(root)>
        return self.s_url_root

    def mfn_fValue(self, s_field_name):
        # Returns the value of the field
        return '|' + s_field_name + '|'

    def mfn_fLabel(self, s_field_name):
        # Returns the label for the field
        return '|' + s_field_name + '|'

    def mfn_date(self):
        # Returns the current date as dd-mmm-yyyy
        return datetime.datetime.now().strftime('%d-%b-%Y')

    def mfn_time(self):
        # Returns the current time as hh:mm:ss
        return datetime.datetime.now().strftime('%H:%M:%S')

    def mfn_sec(self):
        # Returns the current time as seconds since epoch
        return str(time.time())

    def mfn_lang(self, s_text):
        # Returns s_text translated into the current language
        return self.a_lang.translate(s_text)


class MuEvent(QObject):
    # Provides a callback mechanism for a form (without making MuForm dependant on QObject
    # Last Error Code: 30401
    def __init__(self, a_form: MuForm):
        super().__init__()
        self.a_form = a_form
        self.a_form.a_web.page().mainFrame().addToJavaScriptWindowObject("MuEv", self)

    @QtCore.pyqtSlot(str, str, str, result=str)
    def web_event(self, s_event_name, s_param_1, s_param_2):
        # To call this, add this javascript to your form in an appropriate place. The choice of 2 params is somewhat
        # arbitrary, but can be used to pass a name and value from a form to python.
        # MuEv.event('event-name', 'param-1', 'param-2');
        # e.g.
        #   <input type="button" onClick="MuEv.event('event-name', 'param-1', 'param-2')" value="Press Me">
        # In your MuForm form class, define your callback like this (note the 'mev_' prefix!
        #  def mev_event_name(self, s_param_1, s_param_2):
        # By adding mev_ to the method name, we make them easier to find and prevent calling of unintended callbacks
        s_event_name = 'mev_' + s_event_name

        base_info(30401, 'Event for: ' + self.a_form.s_name + '.' + s_event_name
                  + '(' + s_param_1 + ', ' + s_param_2 + ')')

        # check method exists
        if hasattr(self.a_form, s_event_name):
            # The MuForm has a method called 'mev_event_name'. We call it and pass the parameter
            # Declare you method like this:
            #  def mev_event_name(self, s_param_1):
            return getattr(self.a_form, s_event_name)(s_param_1, s_param_2)
        else:
            base_info(30402, 'No handler')
            return '30402'
