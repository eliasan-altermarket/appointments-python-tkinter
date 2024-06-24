"""
Author: Ilias Antonopoulos
eliasan@altermarket.com
www.altermarket.com, www.kalliergo.gr
Appointments Project, 2023-2024 Hellenic Open University
"""

import time
import tkinter as tk
from tkinter import ttk, Menu, messagebox, Toplevel, Frame

class Clock(ttk.Label):
    """
    Creates a clock widget, based on a label
    """
    def __init__(self, root=None, **kw):
        super().__init__(root, **kw)
        self.update_time()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.config(text=current_time)
        self.after(1000, self.update_time)  # Update time every 1 second

if __name__ == "__main__":
    pass