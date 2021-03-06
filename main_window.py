import os
from PySide import QtGui, QtCore
from tabwidget import TabWidget


class MainWindow(QtGui.QMainWindow):
    """ The main window of the app.

    Handles the tab widget and all the actions
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        # variable declaration
        self.m_tabWidget = TabWidget()

        self.m_fileMenu = None
        self.m_fileOpenFileAction = None

        self.m_reloadAction = None

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setUpMenu()

        centralWidget = QtGui.QWidget(self)
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)

        layout.addWidget(self.m_tabWidget)
        centralWidget.setLayout(layout)

        self.m_tabWidget.newTab()

        self.setCentralWidget(centralWidget)

        self.retranslate()

    def setUpMenu(self):
        # File
        self.m_fileMenu = QtGui.QMenu(self.menuBar(), "File")
        self.menuBar().addMenu(self.m_fileMenu)

        self.m_fileMenu.addAction(self.m_tabWidget.newTabAction())
        self.m_fileMenu.addAction(self.m_tabWidget.closeTabAction())

        self.m_fileOpenFileAction = QtGui.QAction(self.m_fileMenu)
        self.m_fileOpenFileAction.setShortcut(QtGui.QKeySequence.Open)
        self.m_fileOpenFileAction.triggered.connect(self.fileOpen)
        self.m_fileMenu.addAction(self.m_fileOpenFileAction)

        self.m_reloadAction = QtGui.QAction(self.m_fileMenu)
        self.m_reloadAction.setShortcut(QtGui.QKeySequence.Refresh)
        self.m_reloadAction.triggered.connect(self.m_tabWidget.reloadCurTab)
        self.m_fileMenu.addAction(self.m_reloadAction)

    def fileOpen(self):
        file_name = QtGui.QFileDialog \
            .getOpenFileName(self, "Open Resource",
                             filter="*.md")
        print(file_name[0])
        if os.path.isfile(file_name[0]):
            self.tabWidget().loadMd(file_name[0])

    def retranslate(self):
        """ Handle the translation, currently hard coded. """
        self.m_fileMenu.setTitle("&File")
        self.m_fileOpenFileAction.setText("&Open File...")
        self.m_reloadAction.setText("&Reload Current Tab")

    def tabWidget(self):
        return self.m_tabWidget
