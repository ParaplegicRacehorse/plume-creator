import os, sys
from pathlib import Path


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

def base_path(sFile):
    # Returns the OS independent path for sFile (which can be a sub folder e.g. 'file.txt' or 'folder/file.txt'
    #print('cwd: ' + os.getcwd())
    return os.path.abspath(os.getcwd() + '/' + sFile)


def base_root_url():
    # Returns the base url - i.e. for the folder the application was started in. Note URLs have / on all OS platforms
    return os.path.abspath(os.path.dirname(sys.argv[0])) + '/'


