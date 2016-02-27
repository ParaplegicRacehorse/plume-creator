#
# MuForm - Support for forms using HTML for gui
#

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo, pyqtSlot, QObject
from PyQt5 import QtWebKitWidgets
import sys
import os
import time
import datetime
from .mu_base import *
from .mu_parse import *

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
        return s_source + '~';


class MuFormList(dict):
    # A collection of MuForms. Useful if you want to sort or arrange the list.
    # Last Error Code: 30101
    def __missing__(self, s_form_name):
        # Called if the requested key is not present. We write an error and return an empty object to allow code
        # to continue (but probably not happily!)
        base_error(30101, 'Undefined MuForm: ' + s_form_name)
        # This empty form allows following code to operate, but it wont find what it is expecting.
        return MuForm('temp')

    def exists(self, s_form_name):
        # Returns true if the specified form name exists in the collection
        return s_form_name in self

    def form(self, s_form_name):
        # returns the MuForm specified by s_form_name
        return self[s_form_name]

    def new(self, s_form_name):
        # Returns a new form and adds it to the dict
        a_dlg = MuForm(s_form_name)
        self[s_form_name] = a_dlg
        return a_dlg


class MuForm:
    # An MuForm is a python form that uses html for its layout
    # We try and isolate ourselves from Qt since we might in future we able to use the webkit directly.
    # Last Error Code: 30301
    def __init__(self):
        # If a_aprent is set (to anothe rMuForm), then this window will use the parent qt window and not create on
        # itself. This is useful for overloading the contents of one window with another (child) window as per the
        # settings where the same qt window is used to display all pages of settings (which allows data sharing too)
        # Some html defaults:
        self.s_url_root = base_root_url()
        self.s_html = '' # Unparsed html
        self.b_dump = False # For debug - see <(dump)>
        self.s_name = 'muForm'
        self.a_lang = MuLate() # Translation support
        # Declare some publics

        self.a_win = None
        self.a_web = None
        self.__gui()

        # Call child setup
        self.setup()

    def __gui(self):
        # Create a new form. s_form_name should be unique else you'll be overwriting something else!
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

    #
    # These methods manipulate the window
    #
    def resize(self, i_x, i_y):
        self.a_win.resize(i_x, i_y)

    def move(self, i_x, i_y):
        self.a_win.move(i_x, i_y)

    def set_title(self, s_title):
        self.a_win.setWindowTitle(s_title)

    def show(self):
        self.a_win.show()

    def close(self):
        self.a_win.destroy()

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
        # Returns the parsed html
        a_parse = MuParse()
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
        print (s_abs_path)
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
    def style(self):
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
    # functions
    #
    def mfn_head(self):
        # Used by a template to insert in the <head> section e.g. style, javascript
        # Usage in html: <(head)>
        return self.head()

    def mfn_style(self):
        # Used by a template to return the stylesheet name
        # Usage in html: <(style)>
        return self.style()

    def mfn_body(self):
        # Used by a template to insert the body
        # Usage in html: <(body)>
        return self.body()

    def mfn_root(self):
        # Returns root folder
        # Usage in html: <(root)>
        return self.s_url_root

    def mfn_dump(self):
        # A pseudo tag to output the html to stdout in refresh(). Put it anywhere in the template or body
        # Usage in html: <(dump)>
        self.b_dump = True
        return ''

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

    @QtCore.pyqtSlot(str, str, result=str)
    def web_event(self, s_event_name, s_param_1):
    #def web_event(self):
        # To call this, add this javascript to your form in an appropriate place
        # MuEv.event('event-name', 'param-1');
        # e.g.
        #   <input type="button" onClick="MuEv.event('event-name', 'param-1')" value="Press Me">
        # In your MuForm form class, define your callback like this (note the 'mev_' prefix!
        #  def mev_event_name(self, s_param_1):
        # By adding mev_ to the method name, we make them easier to find and prevent calling of unintended callbacks
        s_event_name = 'mev_' + s_event_name

        base_info(30401, 'Event for: ' + self.a_form.s_name + '.' + s_event_name + '(' + s_param_1 + ')')

        # check method exists
        if hasattr(self.a_form, s_event_name):
            # The MuForm has a method called 'mev_event_name'. We call it and pass the parameter
            # Declare you method like this:
            #  def mev_event_name(self, s_param_1):
            return getattr(self.a_form, s_event_name)(s_param_1)
        else:
            base_info(30402,'No handler')
            return '30402'