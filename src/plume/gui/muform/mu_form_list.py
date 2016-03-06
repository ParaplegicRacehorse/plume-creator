#
# MuFormList - Support for lists of forms using HTML for gui
# Copyright (C) 2016    Bardi <bardi9@deckertelecom.net>
# Last Error Code: 30101
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
from .mu_form import *


class MuFormList(dict):
    # A collection of MuForms. Useful if you want to sort or arrange the list.
    # Last Error Code: 30101
    def __missing__(self, s_form_name):
        # Called if the requested key is not present. We write an error and return an empty object to allow code
        # to continue (but probably not happily!)
        base_error(30101, 'Undefined MuForm: ' + s_form_name)
        # This empty form allows following code to operate, but it wont find what it is expecting.
        return MuForm()

    def exists(self, s_form_name):
        # Returns true if the specified form name exists in the collection
        return s_form_name in self

    def form(self, s_form_name):
        # returns the MuForm specified by s_form_name
        return self[s_form_name]

    def new(self, s_form_name):
        # Returns a new form and adds it to the dict
        a_frm = MuForm()
        a_frm.s_name = s_form_name
        self[s_form_name] = a_frm
        return a_frm
