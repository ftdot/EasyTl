import tomllib
import os.path
from typing import Any

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject

from settings import *


class QuickMessageBox:
    """Class helps to quickly manage/show messageboxes"""

    def __init__(self,
                 parent: QObject,
                 icon: QMessageBox.Icon,
                 std_buttons: QMessageBox.StandardButtons | QMessageBox.StandardButton):
        """
        :param parent: Parent of the QMessageBox
        :type parent: QObject
        """

        self.msgbox = QMessageBox(parent)
        self.msgbox.setIcon(icon)
        self.msgbox.setStandardButtons(std_buttons)

    def show(self, title: str, message: str) -> int:
        """

        :param title: Title of the QMessageBox
        :param message: Message of the QMessageBox

        :return: Result of the QMessageBox
        :rtype: int
        """

        self.msgbox.setWindowTitle(title)
        self.msgbox.setText(message)

        return self.msgbox.exec_()


def load_instances_list() -> dict[str, Any]:
    """Loads the instances dict

    :returns: Dict with the instances list
    :rtype: dict[str, Any]
    """

    if os.path.exists(ALT_INSTANCES_LIST_PATH):
        # load alt instances list
        with open(ALT_INSTANCES_LIST_PATH, 'rb') as f:
            return tomllib.load(f)

    else:
        # load instances list from default path
        with open(INSTANCES_LIST_PATH, 'rb') as f:
            return tomllib.load(f)


def save_instances_list(_dict: dict[str, Any]):
    """Saves the instances to file

    :param _dict: Dict to be saved
    :type _dict: dict[str, Any]
    """

    if os.path.exists(ALT_INSTANCES_LIST_PATH):
        with open(ALT_INSTANCES_LIST_PATH, 'w') as f:
            toml.dump(_dict, f)
    else:
        with open(INSTANCES_LIST_PATH, 'w') as f:
            toml.dump(_dict, f)
