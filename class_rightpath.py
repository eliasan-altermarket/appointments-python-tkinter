"""
Author: Ilias Antonopoulos
eliasan@altermarket.com
www.altermarket.com, www.kalliergo.gr
Appointments Project, 2023-2024 Hellenic Open University
"""

import os

class Right_path():
    """
    Build and return the right path for a resource file,
    whether the program is run as .py or as an .exe created with PyInstaller.
    """
    def __init__(self, relative_path):
        self.relative_path = relative_path

    def resource_path(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, self.relative_path)