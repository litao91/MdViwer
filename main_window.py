from markdown_view import MarkdownView
from PySide import QtGui, QtCore
from tabwidget import TabWidget
import sys


class MainWindow(QtGui.QMainWindow):
    """ The main window of the app.

    Handles the tab widget and all the actions
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        # variable declaration
        self.m_mdView = None

        self.m_fileMenu = None
        self.m_fileOpenFileAction = None

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setUpMenu()

        self.m_tabWidget = TabWidget()

        self.retranslate()

    def initWebView(self):
        if self.m_mdView is None:
            self.m_mdView = MarkdownView()
        md_str = open(sys.argv[1], 'r').read()
        self.m_mdView.setMarkdown(md_str)
        self.setCentralWidget(self.m_mdView)

    def setUpMenu(self):
        # File
        self.m_fileMenu = QtGui.QMenu(self.menuBar(), "File")
        self.menuBar().addMenu(self.m_fileMenu)

        self.m_fileOpenFileAction = QtGui.QAction(self.m_fileMenu)
        self.m_fileOpenFileAction.setShortcut(QtGui.QKeySequence.Open)
        self.m_fileOpenFileAction.triggered.connect(self.fileOpen)
        self.m_fileMenu.addAction(self.m_fileOpenFileAction)

    def fileOpen(self):
        file_name = QtGui.QFileDialog \
            .getOpenFileName(self, "Open Resource",
                             filter="*.md")
        print(file_name[0])

    def retranslate(self):
        """ Handle the translation, currently hard coded. """
        self.m_fileMenu.setTitle("&File")
        self.m_fileOpenFileAction.setText("&Open File...")

    def tagWidget(self):
        return self.m_tabWidget
