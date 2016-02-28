#
# MuBase - Support functions for MuForms etc
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
import os
import sys


def base_info(i_err, s_msg):
    # Outputs an info msg to stdout
    print('Info: ' + str(i_err) + ' ' + s_msg, file=sys.stdout)


def base_error(i_err, s_msg):
    # Outputs a msg to stderr
    print('Error: ' + str(i_err) + ' ' + s_msg, file=sys.stderr)


def base_form_dir():
    # Returns the sub folder relative to the cwd of the html forms
    return 'gui/html/'


def base_style_dir():
    # Returns the sub folder relative to the cwd of the html forms
    return 'gui/style/'


def base_path(s_file):
    # Returns the OS independent path for sFile (which can be a sub folder e.g. 'file.txt' or 'folder/file.txt'
    return os.path.abspath(os.getcwd() + '/' + s_file)


def base_root_url():
    # Returns the base url - i.e. for the folder the application was started in. Note URLs have / on all OS platforms
    return os.path.abspath(os.path.dirname(sys.argv[0])) + '/'
