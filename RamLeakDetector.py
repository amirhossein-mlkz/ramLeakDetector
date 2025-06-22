import tracemalloc
import keyboard
import logging
from datetime import datetime
import os
import threading
import psutil
import re
import sys
from matplotlib import pyplot as plt
import site
import pickle
import time
import subprocess
from subprocess import CREATE_NEW_CONSOLE

try:
    from .RamLeakRecorder import RamLeakRecorder
    from . import RamLeakPlotter
except:
    from RamLeakRecorder import RamLeakRecorder
    import RamLeakPlotter


class RamLeakDetector:
    def __init__(self, 
                 perion_s = 30, 
                 parent_dirs="ramLeak.logs"):
        
        self.plotter_module_path = RamLeakPlotter.__file__

        
        self.ramLeakRecorder = RamLeakRecorder(
            perion_s=perion_s,
            parent_dirs=parent_dirs,
        )

        keyboard.add_hotkey("ctrl+alt+p", 
                            self.export_plots, 
                            args=(), 
                            suppress=False, 
                            timeout=1, 
                            trigger_on_release=False)


    def export_plots(self,):
        subprocess.Popen(["cmd.exe", "/c", 'python', self.plotter_module_path, '--hist', self.ramLeakRecorder.history_paths ], 
                          creationflags=CREATE_NEW_CONSOLE)



if __name__ == '__main__':
    p  = r'C:\Users\amirh\Desktop\DORSA Projects\MSC_Conveyor - gitlab\ramLeak.logs\RamLeakRecoder\RamLeakDe_2025-06-22_11-34-22\history.hist'
    r = RamLeakDetector()
    
    os.system(f"python \"{r.plotter_module_path}\" --hist=\"{p}\"")
    time.sleep(100)