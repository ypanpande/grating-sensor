
import tkinter as tk
from tkinter import ttk

import pandas as pd
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def main():
    root = tk.Tk()
    filepath = 'D://ttt//data2.csv'
    ADCdata(root, filepath)
    root.mainloop()


class ADCdata:
    def __init__(self, root, filepath):
        self.root = root
        self.root.title('ADC data plot')
        self.root.resizable(0,0)
        self.root.geometry('900x720+30+30')
        self.filepath = filepath
        self.Readcsv()
        self.init_para()
        self.init_gui()
        
    def Readcsv(self):
        self.df = pd.read_csv(self.filepath, header = 0)
        self.df.columns = ['ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','ch13','ch14','ch15','ch16']
        
    def init_para(self):
        self.channel = tk.StringVar()
        self.channel.set('ch1')
        
    def init_gui(self):
        self.setting_panel()
        self.figure_panel()
        
    def setting_panel(self):
        self.setting_frame = tk.Frame(self.root, height = 60 , width  = 880, relief = 'ridge', borderwidth = 1)
        self.setting_frame.place(x = 10, y = 10, width = 880, height = 60)
        
        ttk.Label(self.setting_frame, text = "channels:").place(x = 10, y = 10,  width = 60, height = 30)		
        cch = ttk.Combobox(self.setting_frame, textvariable = self.channel, state = 'readonly')
        cch['value'] = ('ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','ch13','ch14','ch15','ch16')
        cch.place(x = 80, y = 10 , width = 80, height = 30)
        cch.current(0)
        cch.bind('<<ComboboxSelected>>', self.Changeplot)
        
    def figure_panel(self):
        self.figure_frame = tk.Frame(self.root, height = 630 , width  = 880, relief = 'ridge', borderwidth = 1)
        self.figure_frame.place(x = 10, y = 80, width = 880, height = 630)
#        self.Plotchannel()
        self.Embedplot()
#==============================================================================
    #functions
#=================================================================================    
    def Plotchannel(self):
        self.fig = plt.figure(figsize = (7,6))
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.df[self.channel.get()],marker = 'o', markersize = 4, label = self.channel.get())
        self.ax.legend()
        self.ax.grid()
        self.ax.set_xlabel('sample number', fontsize = 14)
        self.ax.set_ylabel('ADC data', fontsize = 14)
        plt.ioff()
        plt.close()
#        return fig
    
    def Embedplot(self):
        
        #embed figure and toolbar
        self.event_canvas_frame = tk.Frame(self.figure_frame)
        self.event_canvas_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        self.Plotchannel()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.event_canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.event_toolbar_frame = tk.Frame(self.figure_frame)
        self.event_toolbar_frame.pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(self.canvas, self.event_toolbar_frame)
        toolbar.update()
        
    def Changeplot(self, event):
        self.ax.clear()
        self.ax.plot(self.df[self.channel.get()],marker = 'o', markersize = 3, label = self.channel.get())
        self.ax.legend()
        self.ax.grid()
        self.ax.set_xlabel('sample number', fontsize = 14)
        self.ax.set_ylabel('ADC data', fontsize = 14)
        self.canvas.draw()
#        try:
##            self.frame_canvas_frame.winfo_exists():
#            self.event_canvas_frame.destroy()
#            self.event_toolbar_frame.destroy()
#            
#            self.Embedplot()
#
#        except:
#            self.Embedplot()
    
    
    
if __name__ == '__main__': main()