#!C:\Users\UserPC\Desktop\ieps_project\pa1\project1\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'chromedriver-binary==90.0.4430.24.0','console_scripts','chromedriver-path'
__requires__ = 'chromedriver-binary==90.0.4430.24.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('chromedriver-binary==90.0.4430.24.0', 'console_scripts', 'chromedriver-path')()
    )
