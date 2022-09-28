import torrent
import sys
from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
torrent.TorrentDownloader.GUI = True
app = QApplication(sys.argv)
install_ui = 'Resources/install.ui'
ui_file = QFile(install_ui)
loader = QUiLoader()
torrent.TorrentDownloader.window = loader.load(ui_file)
ui_file.close()
torrent.TorrentDownloader.window.show()
x = torrent.TorrentDownloader()
sys.exit(app.exec_())