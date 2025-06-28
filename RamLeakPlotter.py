import tracemalloc
import os
import pickle
import argparse
import time


from matplotlib import pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description="A simple script with command line arguments.")
parser.add_argument("--hist", type=str, help="path of history")






class RamLeakPlotter:
    MAX_HISTORY = 500
    def __init__(self, 
                 hist_path = '',
                 ):
        
      
        self.hist_path = hist_path
        self.memory_stats_history:dict[tracemalloc.Traceback, list[int]] = {}


        self.gen_paths()
        

        
        

        

    def gen_paths(self,):
        self.parent_dir = os.path.dirname(self.hist_path)
        self.plots_dir = os.path.join(self.parent_dir, 'plots')
        self.plots_report = os.path.join(self.plots_dir, 'report.txt')
        os.makedirs(self.plots_dir, exist_ok=True)
    
    def load_history(self,):
        if not os.path.exists(self.hist_path):
            print(f"history not founded in this path: {self.hist_path}")
            return False
        try:
            with open(self.hist_path, 'rb') as file:
                self.memory_stats_history = pickle.load(file)
            return True
        except:
            return False
        

    
    def list_stats_to_str(self, my_list:list):
        res = list(map(lambda x:str(x), my_list))
        return '\n'.join(res)
    
    def split_by_char_count_loop(self,text, n):
        result = []
        for i in range(0, len(text), n):
            result.append(text[i:i+n])
        return '\n'.join(result)
    
    def save_plot(self, name:str, stat:tracemalloc.Traceback, sizes:list):
        if len(sizes) < 2:
            return False
        
        tilte = str(stat)
        tilte  = self.split_by_char_count_loop(tilte, 100)
        ys = sizes
        xs = list(range(len(ys)))
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(xs, ys)
        ax.set_title(f"{tilte}")
        fname = str(name) + ".png"
        path = os.path.join(self.plots_dir, fname)
        print(path)
        fig.savefig(path)
        return True
    


    def slope_calculation(self, ys):
        ys = np.array(ys)
        xs = np.arange(len(ys))
        try:
            x = np.expand_dims(xs, axis=-1)
            y = np.expand_dims(ys, axis=-1)
            featurs = np.hstack((np.ones_like(x), x))  # , x**2))
            theta = np.linalg.inv(np.matmul(featurs.transpose(), featurs))
            theta = np.matmul(theta, featurs.transpose())
            theta = np.matmul(theta, y)
            slope = theta[1][0]
            intercept = theta[0]
            return slope, intercept
        except:
            return 0, 0

    def calculate_increasement(self,):
        res = []
        for stat in self.memory_stats_history:
            sizes = self.memory_stats_history[stat]
            slope, _ = self.slope_calculation(sizes)
            res.append((slope, stat))
        res.sort(key=lambda x:x[0], reverse=True)
        return res
    
    def report_gen(self,name:str, stat, sizes:list[int]):
        res = ""
        res = res + "-"*100 + '\n'
        res = res + f"ID:{name}\n"
        res = res + f"stat:{stat}\n"
        res = res + f"sizes:{sizes}\n"
        res = res + "-"*100 + '\n'
        return res




    def export_plots(self,):
        ret = self.load_history()
        if not ret:
            return
        
        increasement = self.calculate_increasement()
        total = len(increasement)

        if os.path.exists(self.plots_report):
            os.remove(self.plots_report)
        
        for i, (slope, stat) in enumerate(increasement):
            sizes = self.memory_stats_history[stat]
            res = self.save_plot(i, stat, sizes)
            text = self.report_gen(i, stat, sizes)
            with open(self.plots_report, 'at') as file:
                file.write(text)

            print('Export plots: ', i+1, '/', total, f'status: {res}')
            

        
        



if __name__ == "__main__":
    pass
    args = parser.parse_args()
    p = r'C:\Users\amirh\Desktop\DORSA Projects\MSC_Conveyor - gitlab\ramLeak.logs\RamLeakRecoder\RamLeakDe_2025-06-22_11-34-22\history.hist'
    print(args.hist)
    rlp = RamLeakPlotter(args.hist)
    rlp.export_plots()
    print('Finished')
    time.sleep(10)
    