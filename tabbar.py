from PySide import QtGui


class TabBar(QtGui.QTabBar):
    def __init__(self, parent):
        super(TabBar, self).__init__()
        self.setParent(parent)

        self.m_showTabBarWhenOneTab = True

    def shoTagBarWhenOneTab(self):
        return self.m_showTabBarWhenOneTab

    def selectTabAction(self):
        index = self.sender().tab()
        self.setCurrentIndex(index)

    def tabSizeHint(self, index):
        sizeHint = QtGui.QTabBar.tabSizeHint(index)
        fm = self.fontMetrics()
        return sizeHint.boundedTo(QtGui.QSize(fm.width('M')) * 18,
                                  sizeHint.height())
