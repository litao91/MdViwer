from PySide import QtGui
from tabbar import TabBar
from markdown_view import MarkdownView


class TabWidget(QtGui.QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()
        self.m_recentlyClosedTabsAction = None
        self.mm_newTabAction = None
        self.m_closeTabAction = None
        self.m_nextTabAction = None
        self.m_previousTabAction = None
        self.addTabButton = None
        self.closeTabButton = None

        self.m_tabBar = TabBar(self)

    def newTab(self):
        self.makeNewTab(True)

    def makeNewTab(self, makeCurrent):
        markdownView = MarkdownView()
        return markdownView
