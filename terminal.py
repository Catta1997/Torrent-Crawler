"""CLI functions"""

import json

# import os
import sys

import torrentelem
from torrent import TorrentDownloader

# text format
bold_text = "\033[1m"
underscore = "\x1b[4m"
reset_clr = "\x1b[0m"
red = "\x1b[31m"
green = "\x1b[32m"
yellow = "\x1b[33m"
blue = "\x1b[34m"
magenta = "\x1b[35m"
cyan = "\x1b[36m"
white = "\x1b[37m"


class TorrentDownloaderCLI:
    """choose magnet from cli"""
    t = TorrentDownloader()

    def __init__(self) -> None:
        TorrentDownloader.setup(self.t)
        if len(sys.argv) == 1:
            name_input = input("Nome Film da cercare: ").strip()
        else:
            name_input = sys.argv[1]
            for elem in sys.argv[2:]:
                name_input += "%20" + elem
        TorrentDownloader.search1377x_request(self.t, str(name_input))
        # print list
        TorrentDownloader.solidtorrents_request(self.t, str(name_input))
        torrent = 1
        TorrentDownloader.torrent_list = self.t.torren_fields
        for elem in TorrentDownloader.torren_fields:
            # write _____________
            print(underscore + " " * 120 + reset_clr + "\n")
            print(f" {bold_text}Torrent {torrent} :{reset_clr}")
            TorrentDownloaderCLI.print_elem(elem)
            torrent += 1
        self.choose()

    @staticmethod
    def print_elem(elem: torrentelem.TorrentElem) -> None:
        """Print torrent element"""
        title_t = elem.name
        min_pos = 0
        max_pos = 95
        print(f" {cyan}TITLE: {title_t[min_pos:max_pos]}{reset_clr}")
        while max_pos < len(title_t):
            min_pos += 95
            max_pos += 95
            print(f" {cyan}       {title_t[min_pos:max_pos]}{reset_clr}")
        print(f" {red}DATE: {elem.date}{reset_clr}")
        print(f" {green}DIM: {str(elem.size)} {elem.file_type}{reset_clr}")
        print(f" {yellow}SEED: {elem.seeders}{reset_clr}")
        print(f" {white}LEECH: {elem.leecher}{reset_clr}")
        print(f" {magenta}TYPE: {elem.file_type}{reset_clr}")

    def choose(self) -> None:
        """Select torrent"""
        # write _____________
        print(underscore + " " * 120 + reset_clr + "\n")
        found = 0
        number = 0
        while found == 0:
            try:
                number = int(input("Choose torrent: "))
            except ValueError:
                print(f"\n{red}Not Valid!!{reset_clr}\n")
                TorrentDownloaderCLI.choose(self)
            found = 1
            number -= 1  # indice di un array
            selected_elem:torrentelem = TorrentDownloader.torren_fields[number]
            TorrentDownloaderCLI.print_elem(selected_elem)
            conf = ""
            while conf.lower() not in ["y", "n"]:
                conf = input("\ny to confirm, n to repeat: ")
            if conf.lower() == "n":
                found = 0
            elif conf.lower() == "y":
                # controllo che number sia una scelta valida:
                if 0 <= number < len(TorrentDownloader.torren_fields):
                    TorrentDownloader.get_magnet(
                        self.t, selected_elem.link, False
                    )
                else:
                    print(f"{red}Not Valid{reset_clr}")


x = TorrentDownloaderCLI()
