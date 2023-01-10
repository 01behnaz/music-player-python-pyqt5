
import sys
from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentPlaylist = QMediaPlaylist()
        self.player = QMediaPlayer()
        # 0- stopped, 1- playing 2-paused
        self.userAction = -1
        self.player.mediaStatusChanged.connect(self.qmp_mediaStatusChanged)
        self.player.stateChanged.connect(self.qmp_stateChanged)
        self.player.positionChanged.connect(self.qmp_positionChanged)
        self.player.volumeChanged.connect(self.qmp_volumeChanged)
        self.player.setVolume(60)

        # Add Status bar
        self.statusBar().showMessage('No Media :: %d' % self.player.volume())
        self.homeScreen()

    def homeScreen(self):
        self.setWindowTitle('Music Player')
        self.setWindowIcon(QIcon('icons8-headphones-60.png'))

        # create Menubar and Toolbar
        self.createMenubar()
        # Add Control Bar
        controlBar = self.addControls()

        centralWidget = QWidget()
        centralWidget.setLayout(controlBar)
        self.setCentralWidget(centralWidget)
        self.resize(400, 200)
        self.show()

    def createMenubar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("QMenuBar{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(255, 255, 255);\n"
                              "}\n")
        filemenu = menubar.addMenu('File')
        filemenu.addAction(self.songInfo())
        filemenu.addAction(self.folderOpen())
        filemenu.addAction(self.exitAction())

    def addControls(self):
        controlArea = QVBoxLayout()
        seekSliderLayout = QHBoxLayout()
        controls = QHBoxLayout()
        playlistCtrlLayout = QHBoxLayout()
        # create buttons
        playBtn = QPushButton('Play')  # btn play
        playBtn.setFixedSize(60, 35)
        playBtn.setStyleSheet("QPushButton{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(255, 255, 255);\n"
                              "    font: 10pt \"MRT_Flow\";\n"
                              "    border-radius: 15px;\n"
                              "}\n"
                              "QPushButton:Hover{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(247, 194, 50);\n"
                              "}")
        pauseBtn = QPushButton('Pause')  # btn pause
        pauseBtn.setFixedSize(60, 35)
        pauseBtn.setStyleSheet("QPushButton{\n"
                               "    color: rgb(51, 51, 51);\n"
                               "    background-color: rgb(255, 255, 255);\n"
                               "    font: 10pt \"MRT_Flow\";\n"
                               "    border-radius: 15px;\n"
                               "}\n"
                               "QPushButton:Hover{\n"
                               "    color: rgb(51, 51, 51);\n"
                               "    background-color: rgb(247, 194, 50);\n"
                               "}")
        stopBtn = QPushButton('Stop')  # btn stop
        stopBtn.setFixedSize(60, 35)
        stopBtn.setStyleSheet("QPushButton{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(255, 255, 255);\n"
                              "    font: 10pt \"MRT_Flow\";\n"
                              "    border-radius: 15px;\n"
                              "}\n"
                              "QPushButton:Hover{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(247, 194, 50);\n"
                              "}")
        volumeDescBtn = QPushButton('V (-)')  # Decrease Volume
        volumeDescBtn.setFixedSize(60, 35)
        volumeDescBtn.setStyleSheet("QPushButton{\n"
                                    "    color: rgb(51, 51, 51);\n"
                                    "    background-color: rgb(255, 255, 255);\n"
                                    "    font: 10pt \"MRT_Flow\";\n"
                                    "    border-radius: 15px;\n"
                                    "}\n"
                                    "QPushButton:Hover{\n"
                                    "    color: rgb(51, 51, 51);\n"
                                    "    background-color: rgb(247, 194, 50);\n"
                                    "}")
        volumeIncBtn = QPushButton('V (+)')  # Increase Volume
        volumeIncBtn.setFixedSize(60, 35)
        volumeIncBtn.setStyleSheet("QPushButton{\n"
                                   "    color: rgb(51, 51, 51);\n"
                                   "    background-color: rgb(255, 255, 255);\n"
                                   "    font: 10pt \"MRT_Flow\";\n"
                                   "    border-radius: 15px;\n"
                                   "}\n"
                                   "QPushButton:Hover{\n"
                                   "    color: rgb(51, 51, 51);\n"
                                   "    background-color: rgb(247, 194, 50);\n"
                                   "}")
        # creating playlist controls
        prevBtn = QPushButton('Prev Song')  # btn prev
        prevBtn.setFixedSize(120, 35)
        prevBtn.setStyleSheet("QPushButton{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(255, 255, 255);\n"
                              "    font: 10pt \"MRT_Flow\";\n"
                              "    border-radius: 15px;\n"
                              "}\n"
                              "QPushButton:Hover{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(247, 194, 50);\n"
                              "}")
        nextBtn = QPushButton('Next Song')  # btn next
        nextBtn.setFixedSize(120, 35)
        nextBtn.setStyleSheet("QPushButton{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(255, 255, 255);\n"
                              "    font: 10pt \"MRT_Flow\";\n"
                              "    border-radius: 15px;\n"
                              "}\n"
                              "QPushButton:Hover{\n"
                              "    color: rgb(51, 51, 51);\n"
                              "    background-color: rgb(247, 194, 50);\n"
                              "}")
        # creating seek slider
        seekSlider = QSlider()
        seekSlider.setMinimum(0)
        seekSlider.setMaximum(100)
        seekSlider.setOrientation(Qt.Horizontal)
        seekSlider.setTracking(False)
        seekSlider.sliderMoved.connect(self.seekPosition)
        seekSliderLabel1 = QLabel('0.00')
        seekSliderLabel2 = QLabel('0.00')
        seekSliderLayout.addWidget(seekSliderLabel1)
        seekSliderLayout.addWidget(seekSlider)
        seekSliderLayout.addWidget(seekSliderLabel2)
        # connect func
        playBtn.clicked.connect(self.playHandler)
        pauseBtn.clicked.connect(self.pauseHandler)
        stopBtn.clicked.connect(self.stopHandler)
        volumeDescBtn.clicked.connect(self.decreaseVolume)
        volumeIncBtn.clicked.connect(self.increaseVolume)
        # add btn to controlslayout
        controls.addWidget(volumeDescBtn)
        controls.addWidget(playBtn)
        controls.addWidget(pauseBtn)
        controls.addWidget(stopBtn)
        controls.addWidget(volumeIncBtn)
        # connect func
        prevBtn.clicked.connect(self.prevItemPlaylist)
        nextBtn.clicked.connect(self.nextItemPlaylist)
        # add btn to playlistCtrlLayout
        playlistCtrlLayout.addWidget(prevBtn)
        playlistCtrlLayout.addWidget(nextBtn)
        # add layouys to controlArea
        controlArea.addLayout(seekSliderLayout)
        controlArea.addLayout(controls)
        controlArea.addLayout(playlistCtrlLayout)
        return controlArea

    def playHandler(self):
        self.userAction = 1
        self.statusBar().showMessage('Playing at Volume %d' % self.player.volume())
        if self.player.state() == QMediaPlayer.StoppedState:
            if self.player.mediaStatus() == QMediaPlayer.NoMedia:
                print(self.currentPlaylist.mediaCount())
                if self.currentPlaylist.mediaCount() != 0:
                    self.player.setPlaylist(self.currentPlaylist)
            elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
                self.player.play()
            elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
                self.player.play()
        elif self.player.state() == QMediaPlayer.PlayingState:
            pass
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()

    def pauseHandler(self):  # pause Btn
        self.userAction = 2
        self.statusBar().showMessage('Paused %s at position %s at Volume %d' %
                                     (self.player.metaData(QMediaMetaData.Title),
                                      self.centralWidget().layout().itemAt(0).layout().itemAt(0).widget().text(),
                                         self.player.volume()))
        self.player.pause()

    def stopHandler(self):  # stopBtn
        self.userAction = 0
        self.statusBar().showMessage('Stopped at Volume %d' % (self.player.volume()))
        if self.player.state() == QMediaPlayer.PlayingState:
            self.stopState = True
            self.player.stop()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.stop()
        elif self.player.state() == QMediaPlayer.StoppedState:
            pass

    def qmp_mediaStatusChanged(self):
        if self.player.mediaStatus() == QMediaPlayer.LoadedMedia and self.userAction == 1:
            durationT = self.player.duration()
            self.centralWidget().layout().itemAt(0).layout().itemAt(
                1).widget().setRange(0, durationT)
            self.centralWidget().layout().itemAt(0).layout().itemAt(2).widget().setText(
                '%d:%02d' % (int(durationT/60000), int((durationT/1000) % 60)))
            self.player.play()

    def qmp_stateChanged(self):
        if self.player.state() == QMediaPlayer.StoppedState:
            self.player.stop()

    def qmp_positionChanged(self, position, senderType=False):
        sliderLayout = self.centralWidget().layout().itemAt(0).layout()
        if senderType == False:
            sliderLayout.itemAt(1).widget().setValue(position)
        # update the text label
        sliderLayout.itemAt(0).widget().setText('%d:%02d' %
                                                (int(position/60000), int((position/1000) % 60)))

    def seekPosition(self, position):
        sender = self.sender()
        if isinstance(sender, QSlider):
            if self.player.isSeekable():
                self.player.setPosition(position)

    def qmp_volumeChanged(self):
        msg = self.statusBar().currentMessage()
        msg = msg[:0] + str(self.player.volume())
        self.statusBar().showMessage(msg)

    def increaseVolume(self):
        vol = self.player.volume()
        vol = min(vol+5, 100)
        self.player.setVolume(vol)

    def decreaseVolume(self):
        vol = self.player.volume()
        vol = max(vol-5, 0)
        self.player.setVolume(vol)

    def fileOpen(self):
        fileAc = QAction('Open File', self)
        fileAc.setShortcut('Ctrl+O')
        fileAc.setStatusTip('Open File')
        return fileAc

    def folderOpen(self):
        folderAc = QAction('Open Folder', self)
        folderAc.setShortcut('Ctrl+D')
        folderAc.setStatusTip(
            'Open Folder (Will add all the files in the folder) ')
        folderAc.triggered.connect(self.addFiles)
        return folderAc

    def addFiles(self):
        folderChoosen = QFileDialog.getExistingDirectory(
            self, 'Open Music Folder', expanduser('~'))
        if folderChoosen != None:
            it = QDirIterator(folderChoosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    print(it.filePath(), fInfo.suffix())
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav'):
                        print('added file ', fInfo.fileName())
                        self.currentPlaylist.addMedia(
                            QMediaContent(QUrl.fromLocalFile(it.filePath())))
                it.next()

    def songInfo(self):
        infoAc = QAction('Info', self)
        infoAc.setShortcut('Ctrl+I')
        infoAc.setStatusTip('Displays Current Song Information')
        infoAc.triggered.connect(self.displaySongInfo)
        return infoAc

    def displaySongInfo(self):
        metaDataKeyList = self.player.availableMetaData()
        fullText = '<table class="tftable" border="0">'
        for key in metaDataKeyList:
            value = self.player.metaData(key)
            fullText = fullText + '<tr><td>' + key + \
                '</td><td>' + str(value) + '</td></tr>'
        fullText = fullText + '</table>'
        infoBox = QMessageBox(self)
        infoBox.setWindowTitle('Detailed Song Information')
        infoBox.setTextFormat(Qt.RichText)
        infoBox.setText(fullText)
        infoBox.addButton('OK', QMessageBox.AcceptRole)
        infoBox.show()

    def prevItemPlaylist(self):
        self.player.playlist().previous()

    def nextItemPlaylist(self):
        self.player.playlist().next()

    def exitAction(self):
        exitAc = QAction('&Exit', self)
        exitAc.setShortcut('Ctrl+Q')
        exitAc.setStatusTip('Exit App')
        exitAc.triggered.connect(self.closeEvent)
        return exitAc

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Message', 'Press Yes to Close.', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            qApp.quit()
        else:
            try:
                event.ignore()
            except AttributeError:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
