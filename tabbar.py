from PySide import QtGui, QtCore


class TabBar(QtGui.QTabBar):
    loadMd = QtCore.Signal(str)
    newTab = QtCore.Signal()

    def __init__(self, parent):
        super(TabBar, self).__init__()
        self.setParent(parent)
        self.setAcceptDrops(True)
        self.setElideMode(QtCore.Qt.ElideRight)
        self.setUsesScrollButtons(True)
        self.customContextMenuRequested.connect(self.contextMenuRequested)

        self.m_showTabBarWhenOneTab = True
        self.m_viewTabBarAction = QtGui.QAction(self)
        self.updateViewToolBarAction()
        self.setMovable(True)

        # Signals

    def showTabBarWhenOneTab(self):
        return self.m_showTabBarWhenOneTab

    def setShowTabBarWhenOneTab(self, enabled):
        self.m_showTabBarWhenOneTab = enabled

    def viewTabBarAction(self):
        return self.m_viewTabBarAction

    def freeSide(self):
        side = self.style().styleHint(
            QtGui.QStyle.SH_TabBar_CloseButtonPosition,
            0, self)
        if side == QtGui.QTabBar.LeftSide:
            return QtGui.QTabBar.RightSide
        else:
            return QtGui.QTabBar.LeftSide

    def updateViewToolBarAction(self):
        show = self.showTabBarWhenOneTab()
        if(self.count() > 1):
            show = True
        text = ''
        if not show:
            text = "Show Tab Bar"
        else:
            text = "Hide Tab Bar"
        self.m_viewTabBarAction.setText(text)

    def viewTabBar(self):
        self.setShowTabBarWhenOneTab(not self.showTabBarWhenOneTab())
        self.updateViewToolBarAction

    def selectTabAction(self):
        index = self.sender().tab()
        self.setCurrentIndex(index)

    def tabSizeHint(self, index):
        sizeHint = QtGui.QTabBar.tabSizeHint(index)
        fm = self.fontMetrics()
        return sizeHint.boundedTo(QtGui.QSize(fm.width('M')) * 18,
                                  sizeHint.height())

    def cloneTabSlot(self):
        action = self.sender()
        if self is not None:
            index = action.data().toInt()
            self.cloneTab.emit(index)

    def closeTabSlot(self):
        action = self.sender()
        if self is not None:
            index = action.data().toInt()
            self.closeTab.emit(index)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton \
                and self.tabAt(event.pos()) is -1:
            return
        super(QtGui.QTabBar, self).mouseDoubleClickEvent

    @QtCore.Slot(QtCore.QPoint)
    def contextMenuRequested(self, point):
        print("context menu requested")
