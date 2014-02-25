#!/usr/bin/python3
import sys
from PySide import QtGui
from MarkdownView import MarkdownView


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        self.mdView = None
        super(MainWindow, self).__init__()
        self.initWebView()

    def initWebView(self):
        if self.mdView is None:
            self.mdView = MarkdownView()
        md_str = open(sys.argv[1], 'r').read()
        self.mdView.setMarkdown(md_str)
        self.setCentralWidget(self.mdView)


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
