
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



class RamLeakRecorder:
    MAX_HISTORY = 500
    def __init__(self, 
                 perion_s = 30, 
                 parent_dirs="ramLeak.logs"):
        
        self.perion_s = perion_s
        self.parent_dirs = parent_dirs
        self.export_dirs = ''
        self.history_paths = ''
        
        self.__started_flag = False
        self.memory_stats_history:dict[tracemalloc.Traceback, list[int]] = {}
        
        
        keyboard.add_hotkey("ctrl+alt+s", 
                            self.start, 
                            args=(), 
                            suppress=False, 
                            timeout=1, 
                            trigger_on_release=False)
        

        
        keyboard.add_hotkey("ctrl+alt+e", 
                            self.save_hist, 
                            args=(), 
                            suppress=False, 
                            timeout=1, 
                            trigger_on_release=False)
        
        
        

        
        
    def stop(self,):
        self.__started_flag = False
        tracemalloc.stop()

    def start(self,):
        self.gen_paths()

        tracemalloc.start()
        self.__started_flag = True
        module_to_exclude_path = []
        module_to_exclude_path.append( sys.modules[__name__].__file__)
        module_to_exclude_path.append( sys.modules[tracemalloc.__name__].__file__)
        # Create a filter to exclude the specific module
        self.trace_filters = [ tracemalloc.Filter(False, sys.modules[__name__].__file__),
                              tracemalloc.Filter(False, sys.modules[tracemalloc.__name__].__file__),
                              ]
        for path in site.getsitepackages():
            self.trace_filters.append( 
                tracemalloc.Filter(False, os.path.join(path, '*') )
                                   )
            
        self.start_snapshot_timer()
    
    def gen_paths(self,):
        date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        folder = f"RamLeakDe_{date_str}" 

        self.export_dirs = os.path.join(self.parent_dirs, 'RamLeakRecoder', folder)
        self.history_paths = os.path.join(self.export_dirs, 'history.hist')
        os.makedirs(self.export_dirs, exist_ok=True)
        


    def start_snapshot_timer(self,):
        timer = threading.Timer(self.perion_s, self.snapshot_timer_event, )
        timer.start() # Start the timer thread


    def memory_snapshot(self,) -> tuple[ list[tuple[tracemalloc.Statistic, int]], list[tracemalloc.Statistic]]:
        if not self.__started_flag:
            return
        snapshot = tracemalloc.take_snapshot().filter_traces(self.trace_filters)
        stats = snapshot.statistics('lineno')
        for stat in stats:
            if stat.traceback in self.memory_stats_history:
                self.memory_stats_history[stat.traceback].append(stat.size)
                
            else:
                self.memory_stats_history[stat.traceback] = [stat.size]
            
    def save_hist(self,):
        if not self.__started_flag:
            return
        threading.Thread(target=self.__save_hist).start()

    def __save_hist(self,):
        with open(self.history_paths, 'wb') as file:
            pickle.dump(self.memory_stats_history, file)
            return True
        return False

    def snapshot_timer_event(self, ):
        if not self.__started_flag:
            return
        self.start_snapshot_timer()
        self.memory_snapshot()






if __name__ == '__main__':
    rec = RamLeakRecorder()
    rec.start()
    import time
    while True:
        time.sleep(0.5)