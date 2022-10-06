import torrent
import sys
# GUI import
try:
    from PySide2.QtCore import QFile, QCoreApplication, Qt
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import QApplication
except ModuleNotFoundError:
    bold_text = "\033[1m"
    red = "\x1b[31m"
    reset_clr = "\x1b[0m"
    print(f"{bold_text}{red}Installa requirments_gui.txt{reset_clr}")
    sys.exit(0)

torrent.TorrentDownloader.GUI = True
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
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
