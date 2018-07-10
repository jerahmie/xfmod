#!/usr/bin/env python3
"""
TK-based GUI interface for vopgen export.
"""
import queue
import threading
from time import sleep
import tkinter as tk
from tkinter import ttk


class vopgen_gui(object):
    """
    Class to represent the tkinter-based vopgen exporter
    """
    def __init__(self, master):
        self.master = master
        self.master.title("XFmod Vopgen Export")
        self.label = ttk.Label(master, text = "Vopgen Exporter", 
                              font = ("Arial", 16))
        self.label.grid(row = 0, column = 1)

        self.process_button = ttk.Button(master, text = "Export",
                                         command = self.export_vopgen)
        self.process_button.grid(row = 4, column = 0)
        self.quit_button = ttk.Button(master, text = "Quit",
                                      command = self.close_window)
        
        self.quit_button.grid(row = 4, column = 2)
        

    def export_vopgen(self):
        print("exporting vopgen....")
        sleep(60)
        print("Done.")

    def close_window(self):
        self.master.quit()
        
def main():
    vg = vopgen_gui(tk.Tk())
    tk.mainloop()

if __name__ == '__main__':
    main()
