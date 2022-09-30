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
magnet_ui = 'Resources/show.ui'
ui_file = QFile(install_ui)
ui_magnet = QFile(magnet_ui)
loader = QUiLoader()
torrent.TorrentDownloader.window = loader.load(ui_file)
torrent.TorrentDownloader.magnet_window = loader.load(magnet_ui) 
ui_file.close()
ui_magnet.close()
torrent.TorrentDownloader.window.show()
x = torrent.TorrentDownloader()
sys.exit(app.exec_())