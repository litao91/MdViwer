from PySide import QtCore
import os
import time


class MdFileModel(QtCore.QObject):
    fileModified = QtCore.Signal()

    def __init__(self, path, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.m_fPath = path
        self.m_fsWatcher = QtCore.QFileSystemWatcher()
        self.m_fsWatcher.addPath(path)
        self.m_fsWatcher.fileChanged.connect(self.onFileChange)

    def read(self):
        handle = open(self.m_fPath, 'r')
        fStr = handle.read()
        handle.close()
        return fStr

    def absPath(self):
        return os.path.dirname(self.m_fPath)

    def onFileChange(self, path):
        self.watcher = WaitForFile(self.m_fPath)
        self.watcher.fileReady.connect(self.onFileReady,
                                       QtCore.Qt.QueuedConnection)
        self.watcher.start()

    def onFileReady(self):
        print("file ready!")
        self.m_fsWatcher.addPath(self.m_fPath)
        self.fileModified.emit()


class WaitForFile(QtCore.QThread):
    fileReady = QtCore.Signal()

    def __init__(self, file_path):
        QtCore.QThread.__init__(self)
        self.m_fPath = file_path

    def run(self):
        for i in range(10):
            time.sleep(2)
            if os.path.isfile(self.m_fPath):
                self.fileReady.emit()
                break
