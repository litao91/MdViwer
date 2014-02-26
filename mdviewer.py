#!/usr/bin/python3

""" A very simple markdown viewer.

The naming follows the Qt/C++ convention. Since PySide also
use the names from Qt. Probably I'll port it into C++ someday.
"""

import sys
from PySide import QtGui
from main_window import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
