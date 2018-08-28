#!/usr/bin/env python3
"""
TK-based GUI interface for vopgen export.
"""
import os
import sys
import queue
import threading
from time import sleep
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from threading import Thread
import multiprocessing as mp
import multiprocessing.queues as mpq
import xfmod

class StdoutQueue(mpq.Queue):
    """
    Use a multiprocessing queue to simulate stdout
    """
    def __init__(self, *args, **kwargs):
        ctx = mp.get_context()
        super(StdoutQueue, self).__init__(*args, **kwargs, ctx=ctx)

    def write(self, msg):
        self.put(msg)

    def flush(self):
        sys.__stdout__.flush()

def text_catcher(text_widget, queue):
    """
    Helper function to tunnel queue text to text widget. 
    """
    while True:
        text_widget.insert(tk.END, queue.get())
        text_widget.see(tk.END)

class VopgenGUI(object):
    """
    Class to represent the tkinter-based vopgen exporter
    """
    def __init__(self, master):
        self.initial_dir = os.getenv("HOME")
        self.master = master
        self.compute_p = None  # compute process

        # GUI element: Title
        self.master.title("XFmod Vopgen Export")
        ttk.Label(self.master, text = "Vopgen Exporter", 
                  font = ("Arial", 16)).grid(row = 0, column = 0)
        ttk.Label(self.master, text = "XF Input Project: ", 
                  font = ("Arial", 12)).grid(row = 1, column = 0)
        self.entry_xf_proj = ttk.Entry(self.master, text = "", exportselection = 0)
        self.entry_xf_proj.grid(row = 1, column = 1, columnspan = 2, sticky=tk.W+tk.E)

        ttk.Label(self.master, text = 'origin (mm)',
                  font = ("Arial", 10)).grid(row = 3, column = 0)
        ttk.Label(self.master, text = 'x0',
                  font = ("Arial", 10)).grid(row = 2, column = 1)
        ttk.Label(self.master, text = 'y0',
                  font = ("Arial", 10)).grid(row = 2, column = 2)
        ttk.Label(self.master, text = 'z0',
                  font = ("Arial", 10)).grid(row = 2, column = 3)
        self.entry_x0 = ttk.Entry(self.master, text = "", exportselection = 0)
        self.entry_x0.grid(row = 3, column = 1)
        self.entry_y0 = ttk.Entry(self.master, text = "", exportselection = 0)
        self.entry_y0.grid(row = 3, column = 2)
        self.entry_z0 = ttk.Entry(self.master, text = "", exportselection = 0)
        self.entry_z0.grid(row = 3, column = 3)

        ttk.Label(self.master, text = 'resolution (mm)', 
                  font = ("Arial", 10)).grid(row = 5, column = 0)
        ttk.Label(self.master, text = 'dx',
                  font = ("Arial", 10)).grid(row = 4, column = 1)
        ttk.Label(self.master, text = 'dy',
                  font = ("Arial", 10)).grid(row = 4, column = 2)
        ttk.Label(self.master, text = 'dz',
                  font = ("Arial", 10)).grid(row = 4, column = 3)

        self.entry_dx = ttk.Entry(self.master, text = "", exportselection = 0)
        self.entry_dx.grid(row = 5, column = 1)
        self.entry_dy = ttk.Entry(self.master, text = "", exportselection = 0)
        self.entry_dy.grid(row = 5, column = 2)
        self.entry_dz = ttk.Entry(self.master, text = "", exportselection = 0)
        self.entry_dz.grid(row = 5, column = 3)

        # GUI element: text output window
        self.frame = tk.Frame(master)
        self.frame.grid(row = 6, column = 0, columnspan = 7)
        self.text_box = ScrolledText(self.frame)
        self.text_box.pack()

        # GUI element: control buttons
        self.proj_button = ttk.Button(self.master, text = "Select",
                                      command = self.choose_project)
        self.proj_button.grid(row = 1, column = 3)
        self.process_button = ttk.Button(self.master, text = "Export",
                                         command = self.export_vopgen)
        self.process_button.grid(row = 7, column = 1)
        self.stop_button = ttk.Button(self.master, text = "Stop",
                                      command = self.stop_vopgen)
        self.stop_button.grid(row = 7, column = 2)
        self.quit_button = ttk.Button(self.master, text = "Quit",
                                      command = self.close_window)
        self.quit_button.grid(row = 7, column = 3)

        # Instantiate and start text monitor
        self.q = StdoutQueue()
        monitor = Thread(target = text_catcher, args = (self.text_box, self.q))
        monitor.daemon = True
        monitor.start()

        # Instantiate the process monitor
        p_monitor = Thread(target = self.process_monitor, args=())
        p_monitor.daemon = True
        p_monitor.start()

        # Redirect stdout to tkinter textbox
        sys.stdout = self.q

    def export_vopgen(self):
        """
        Execute vopgen exporter process.
        """
        self.process_button['state'] = 'disabled'
        print("Processing XFdtd Project: ", self.entry_xf_proj.get())
        self.compute_p = mp.Process(target=worker_function, args =(self.q,))
        self.compute_p.start()
        #self.process_button['state'] = 'normal'

    def stop_vopgen(self):
        """
        Stop the vopgen exporter and reset
        """
        if self.compute_p is not None:
            if self.compute_p.is_alive():
                self.compute_p.terminate()
            self.compute_p.join()
            self.process_button['state'] = 'normal'

    def choose_project(self):
        """
        Choose the XF project directory.
        """
        directory_path = filedialog.askdirectory(mustexist = True,
                                                 initialdir = self.initial_dir,
                                                 title = "XFdtd Project Path")
        print("Found project path: ", directory_path)
        par_dir, proj_dir = os.path.split(directory_path)
        self.initial_dir = par_dir
        self.entry_xf_proj.delete(0, 'end')
        self.entry_xf_proj.insert(0, directory_path)

        return directory_path
    
    def close_window(self):
        """
        close main window and exit.
        """
        self.master.quit()
        if self.compute_p is not None:
            if self.compute_p.is_alive():
                self.compute_p.terminate()
            self.compute_p.join()

    def process_monitor(self):
        """
        check the compute process. If not alive, join and reset gui.
        """
        while True:
            sleep(0.5)
            if (self.compute_p is not None) and (self.compute_p.exitcode == 0):
                self.compute_p.join()
                self.process_button['state'] = 'normal'

            


def worker_function(q):
    """
    wrapper for worker function.
    """
    sys.stdout = q
    print("in worker function")
    for i in range(10):
        sleep(1)
        print(i)

if __name__ == '__main__':
    vg = VopgenGUI(tk.Tk())
    tk.mainloop()
