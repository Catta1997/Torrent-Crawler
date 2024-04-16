"""GUI functions"""

import sys
from random import SystemRandom
import torrentelem
from torrent import TorrentDownloader

# text format
bold_text = "\033[1m"
red = "\x1b[31m"
# GUI import
try:
    from PySide6.QtCore import QFile, QCoreApplication, Qt, QObject, QEvent
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication, QLabel, QCheckBox, QPushButton, QLineEdit, QTableWidgetItem, \
        QTableWidget
    from PySide6.QtGui import QIcon, QPixmap, QKeyEvent
except ModuleNotFoundError:
    bold_text = "\033[1m"
    red = "\x1b[31m"
    reset_clr = "\x1b[0m"
    print(f"{bold_text}{red}Install requirments_gui.txt{reset_clr}")
    sys.exit(1)


class TorrentDownloaderGUI:
    """Download Torrent GUI"""
    tabella = None
    t = TorrentDownloader()
    titolo: QLineEdit
    cerca: QPushButton
    add: QCheckBox
    seleziona: QPushButton
    tabella: QTableWidget

    def __init__(self) -> None:
        """initialize variables"""
        self.autoadd = None
        self.selected_elem = None
        selfw = self
        self.t.setup()

        class KeyPressEater(QObject):
            """event filter """

            @staticmethod
            def eventFilter(widget, event: QKeyEvent) -> bool:
                """catch enter key"""
                if event.type() == QEvent.KeyPress:
                    key = event.key()
                    if key == Qt.Key_Return:
                        TorrentDownloaderGUI.avvia_ricerca(
                            selfw)
                        return True
                return False

        TorrentDownloaderGUI.filtro = KeyPressEater()
        self.titolo = TorrentDownloaderGUI.window.findChild(QLineEdit, "titolo")
        self.cerca = TorrentDownloaderGUI.window.findChild(QPushButton, "cerca")
        self.add = TorrentDownloaderGUI.window.findChild(QCheckBox, "add")
        TorrentDownloaderGUI.cerca.clicked.connect(
            lambda: TorrentDownloaderGUI.avvia_ricerca(self))
        TorrentDownloaderGUI.titolo.installEventFilter(self.filtro)

    @staticmethod
    def print_elem_gui(elem: torrentelem.TorrentElem, torrent: int) -> None:
        """insert torrent element in table"""
        title_t = elem.name
        min_pos = 0
        max_pos = 70
        if max_pos < len(title_t):
            TorrentDownloaderGUI.tabella.setItem(torrent, 0, QTableWidgetItem(
                (title_t[min_pos:max_pos] + "\n" + title_t[max_pos:140])))
        else:
            TorrentDownloaderGUI.tabella.setItem(
                torrent, 0, QTableWidgetItem(title_t))
        TorrentDownloaderGUI.tabella.setItem(
            torrent, 1, QTableWidgetItem(f"{str(elem.size)} {elem.file_type}"))
        TorrentDownloaderGUI.tabella.setItem(
            torrent, 2, QTableWidgetItem(elem.seeders))
        TorrentDownloaderGUI.tabella.setItem(
            torrent, 3, QTableWidgetItem(elem.leecher))
        TorrentDownloaderGUI.tabella.setItem(
            torrent, 4, QTableWidgetItem(elem.file_type))
        TorrentDownloaderGUI.tabella.setItem(
            torrent, 5, QTableWidgetItem(elem.date))
        TorrentDownloaderGUI.tabella.resizeColumnsToContents()
        TorrentDownloaderGUI.tabella.resizeRowsToContents()

    def avvia_ricerca(self) -> None:
        """avvio ricerca GUI"""
        name_input = self.titolo.text()
        self.t.search1377x_request(str(name_input))
        # populate tabel
        torrent = 1
        self.tabella: QTableWidget = TorrentDownloaderGUI.window.findChild(
            QTableWidget, "tableWidget")
        self.seleziona: QPushButton = TorrentDownloaderGUI.window.findChild(
            QPushButton, "select")
        TorrentDownloaderGUI.seleziona.clicked.connect(
            lambda: TorrentDownloaderGUI.get_selected_element(self))
        TorrentDownloaderGUI.tabella.clearContents()
        TorrentDownloaderGUI.tabella.setRowCount(0)
        QApplication.processEvents()
        for elem in self.t.torren_fields:
            pos = torrent - 1
            TorrentDownloaderGUI.tabella.insertRow(pos)
            TorrentDownloaderGUI.print_elem_gui(elem, pos)
            torrent += 1

    def get_selected_element(self) -> None:  # this self is TorrentDownloader
        """get list of selected row in GUI"""
        # GUI (first time only)
        self.autoadd = TorrentDownloaderGUI.add.isChecked()
        # get multiple selection
        items = TorrentDownloaderGUI.tabella.selectedItems()
        for item in items:
            # only 1 item in a row
            if item.column() == 1:
                # start download with each selected row
                self.selected_elem: torrentelem.TorrentElem = self.t.torren_fields[item.row()]
                self.t.get_magnet(self.selected_elem.magnet, self.t.gui)


# Winow setup
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)
rand = SystemRandom()
icon = rand.randrange(1, 15)
app.setWindowIcon(QIcon(f"Resources/icon_{icon}.png"))
install_ui = 'Resources/install.ui'
ui_file = QFile(install_ui)
loader = QUiLoader()
TorrentDownloaderGUI.window = loader.load(ui_file)
TorrentDownloaderGUI.logo = TorrentDownloaderGUI.window.findChild(
    QLabel, 'logo')
TorrentDownloaderGUI.window.setWindowTitle('TorrentDownloader')
pixmap = QPixmap('Resources/1280px-1337X_logo.svg.png')
TorrentDownloaderGUI.logo.setPixmap(pixmap)
ui_file.close()
x = TorrentDownloaderGUI()
TorrentDownloaderGUI.window.show()
sys.exit(app.exec_())
