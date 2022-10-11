import torrent
import sys
from random import randrange
# GUI import
try:
    from PySide2.QtCore import QFile, QCoreApplication, Qt
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import QApplication, QLabel
    from PySide2.QtGui import QIcon, QPixmap
except ModuleNotFoundError:
    bold_text = "\033[1m"
    red = "\x1b[31m"
    reset_clr = "\x1b[0m"
    print(f"{bold_text}{red}Install requirments_gui.txt{reset_clr}")
    sys.exit(0)

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
app = QApplication(sys.argv)

icon = randrange(1,15)
app.setWindowIcon(QIcon(f"Resources/icon_{icon}.png"))
install_ui = 'Resources/install.ui'
magnet_ui = 'Resources/show.ui'
ui_file = QFile(install_ui)
ui_magnet = QFile(magnet_ui)
loader = QUiLoader()
torrent.TorrentDownloader.window = loader.load(ui_file)
torrent.TorrentDownloader.magnet_window = loader.load(magnet_ui)
torrent.TorrentDownloader.logo = torrent.TorrentDownloader.window.findChild(QLabel, 'logo')
torrent.TorrentDownloader.window.setWindowTitle('TorrentDownloader')
pixmap = QPixmap('Resources/1280px-1337X_logo.svg.png')
torrent.TorrentDownloader.logo.setPixmap(pixmap)
ui_file.close()
ui_magnet.close()
x = torrent.TorrentDownloader(True)
torrent.TorrentDownloader.window.show()
sys.exit(app.exec_())
