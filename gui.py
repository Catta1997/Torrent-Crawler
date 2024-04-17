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
    t: TorrentDownloader = TorrentDownloader()
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
        self.t.setup(True)

        class KeyPressEater(QObject):
            """event filter """

            def eventFilter(self, widget, event: QKeyEvent) -> bool:
                """catch enter key"""
                if event.type() == QEvent.KeyPress:
                    key = event.key()
                    if key == Qt.Key_Return:
                        selfw.avvia_ricerca()
                        return True
                return False
        self.filtro = KeyPressEater()
        self.titolo = self.window.findChild(QLineEdit, "titolo")
        self.cerca = self.window.findChild(QPushButton, "cerca")
        self.add = self.window.findChild(QCheckBox, "add")
        self.cerca.clicked.connect(
            lambda: self.avvia_ricerca())
        self.titolo.installEventFilter(self.filtro)

    def print_elem_gui(self, elem: torrentelem.TorrentElem, torrent: int) -> None:
        """insert torrent element in table"""
        title_t = elem.name
        min_pos = 0
        max_pos = 70
        if max_pos < len(title_t):
            self.tabella.setItem(torrent, 0, QTableWidgetItem(
                (title_t[min_pos:max_pos] + "\n" + title_t[max_pos:140])))
        else:
            self.tabella.setItem(
                torrent, 0, QTableWidgetItem(title_t))
        self.tabella.setItem(
            torrent, 1, QTableWidgetItem(f"{str(elem.size)} {elem.file_type}"))
        self.tabella.setItem(
            torrent, 2, QTableWidgetItem(elem.seeders))
        self.tabella.setItem(
            torrent, 3, QTableWidgetItem(elem.leecher))
        self.tabella.setItem(
            torrent, 4, QTableWidgetItem(elem.file_type))
        self.tabella.setItem(
            torrent, 5, QTableWidgetItem(elem.date))
        self.tabella.resizeColumnsToContents()
        self.tabella.resizeRowsToContents()

    def avvia_ricerca(self) -> None:
        """avvio ricerca GUI"""
        name_input = self.titolo.text()
        self.t.search1377x_request(str(name_input))
        # populate tabel
        torrent = 1
        self.tabella: QTableWidget = self.window.findChild(
            QTableWidget, "tableWidget")
        self.seleziona: QPushButton = self.window.findChild(
            QPushButton, "select")
        self.seleziona.clicked.connect(
            lambda: self.get_selected_element())
        self.tabella.clearContents()
        self.tabella.setRowCount(0)
        QApplication.processEvents()
        for elem in self.t.torren_fields:
            pos = torrent - 1
            self.tabella.insertRow(pos)
            self.print_elem_gui(elem, pos)
            torrent += 1

    def show_magnet(self, str_magnet: str) -> None:
        """show magnet link on window"""
        from PySide6.QtCore import QFile
        from PySide6.QtUiTools import QUiLoader
        from PySide6.QtWidgets import QTextEdit
        text: QTextEdit = self.magnet_window.findChild(
            QTextEdit, "magnet_link")
        text.insertPlainText(str_magnet)
        text.insertPlainText("\n")
        text.insertPlainText("\n")
        self.magnet_window.show()

    def get_selected_element(self) -> None:  # this self is TorrentDownloader
        """get list of selected row in GUI"""
        # GUI (first time only)
        self.autoadd = self.add.isChecked()
        # get multiple selection
        items = self.tabella.selectedItems()
        for item in items:
            # only 1 item in a row
            if item.column() == 1:
                # start download with each selected row
                selected_elem: torrentelem.TorrentElem = self.t.torren_fields[item.row()]
                selected_elem.get_magnet()
                self.t.start(selected_elem.magnet)
                self.show_magnet(selected_elem.magnet)



if __name__ == "__main__":
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

    loader = QUiLoader()
    magnet_ui = 'Resources/show.ui'
    ui_magnet = QFile(magnet_ui)
    TorrentDownloaderGUI.magnet_window = loader.load(magnet_ui)
    ui_magnet.close()
    x = TorrentDownloaderGUI()
    TorrentDownloaderGUI.window.show()
    sys.exit(app.exec_())
