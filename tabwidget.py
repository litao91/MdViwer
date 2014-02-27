from PySide import QtGui, QtCore
from tabbar import TabBar
from markdown_view import MarkdownView


class TabWidget(QtGui.QTabWidget):
    tabChanged = QtCore.Signal()
    lastTabClosed = QtCore.Signal()

    def __init__(self):
        QtGui.QTabWidget.__init__(self)
        # QtCore.QObject.__init__(self)
        # Signals

        self.m_recentlyClosedTabsAction = None
        self.mm_newTabAction = None
        self.m_closeTabAction = None
        self.m_nextTabAction = None
        self.m_previousTabAction = None
        self.addTabButton = None
        self.closeTabButton = None

        self.m_tabBar = TabBar(self)

        # Actions
        self.m_newTabAction = QtGui.QAction(self)
        self.m_newTabAction.setShortcuts(QtGui.QKeySequence.AddTab)
        self.m_newTabAction.triggered.connect(self.newTab)

        self.m_closeTabAction = QtGui.QAction(self)
        self.m_closeTabAction.setShortcuts(QtGui.QKeySequence.Close)
        self.m_closeTabAction.triggered.connect(self.closeTab)
        self.retranslate()

    def newTabAction(self):
        return self.m_newTabAction

    def closeTabAction(self):
        return self.m_closeTabAction

    def mdView(self, index):
        widget = self.widget(index)
        return widget

    def newTab(self):
        self.makeNewTab(True)

    def makeNewTab(self, makeCurrent):
        markdownView = MarkdownView()
        markdownView.mdTitleChanged.connect(self.mdViewHeaderChanged)
        self.addTab(markdownView, markdownView.getMdTitleText())
        self.setCurrentWidget(markdownView)
        self.tabChanged.emit()
        return markdownView

    def closeTab(self, index=-1):
        """ When index is -1, index chooses the current tab. """
        print("closing tab")
        if index < 0:
            index = self.currentIndex()
        if index < 0 or index >= self.count():
            return

        self.removeTab(index)
        self.tabChanged.emit()
        if self.count() == 0:
            self.lastTabClosed.emit()

    def loadMd(self, file_path):
        mdView = self.getView(self.currentMdView())
        if mdView is not None:
            mdView.loadMd(file_path)

    def currentMdView(self):
        return self.mdView(self.currentIndex())

    def getView(self, currentView):
        mdView = self.makeNewTab(True)
        mdView.setFocus()
        return mdView

    def retranslate(self):
        self.m_closeTabAction.setText('&Close Tab')
        self.m_newTabAction.setText('&New Tab')

    def mdViewHeaderChanged(self, title):
        print("changing title: " + title)
        mdView = self.sender()
        index = self.indexOf(mdView)
        if index == -1:
            return
        self.setTabText(index, title)
        self.setTabToolTip(index, title)
