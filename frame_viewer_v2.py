
#import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
from IQsample4times_frame_class_v2 import GratingSensor
from ADCdata_class import ADCdata

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.figure import Figure
#import matplotlib.pyplot as plt

#import pandas as pd
#import numpy as np
#import datetime

def main():
    root = tk.Tk()
    FrameView(root)
    root.mainloop()

class FrameView():
    def __init__(self, root, default_datafile = 'D://ttt'):
        self.root = root
        self.root.geometry("1580x870+30+30")
        self.root.resizable(0,0)
        self.root.title('Grating Sensor Frame View')
        
        self.default_datafile = default_datafile 
        self.init_para()
        self.init_gui()
    
    def init_para(self):
        self.nchannel = tk.IntVar()
        self.nchannel.set(8)    
        self.nline = tk.IntVar()
        self.nline.set(8)  
        self.triggerlen = tk.IntVar()
        self.triggerlen.set(20)
        self.pointsamplenum = tk.IntVar()  
        self.pointsamplenum.set(160)    
        self.pvalidnum = tk.IntVar()
        self.pvalidnum.set(100)
        self.framepausenum = tk.IntVar()
        self.framepausenum.set(688)
        self.nframe = tk.IntVar()
        self.nframe.set(1) 
        self.bits = tk.IntVar()
        self.bits.set(14)
        #self.plottype = tk.StringVar()
        #self.plottype.set('choose plot type')
    def init_gui(self):
        self.create_parameter_setting_panel()
        self.create_frame_list_panel()
        self.create_frame_display_panel()
    
    def create_parameter_setting_panel(self):
        self.source_display_frame = tk.Frame(self.root, height = 850 , width  = 250, relief = 'ridge', borderwidth = 1)
        self.source_display_frame.place(x = 10, y = 10, width = 250, height = 850)
        
        s = ttk.Style()
        s.configure('my.TButton', font = ('Helvetica', 12), foreground = 'dark green')
        bsource = ttk.Button(self.source_display_frame, text = "Choose Datafile:", style = 'my.TButton', command = self.datafile_input)
        bsource.place(x = 5, y = 5, width = 130, height = 30)		

        self.lsource = ttk.Label(self.source_display_frame, text = self.default_datafile, background = "white", wraplength = 220)
        self.lsource.place(x = 5, y = 40, width = 235, height = 60)

        bdata = ttk.Button(self.source_display_frame, text = "Show Data", style = 'my.TButton', command = self.show_ADCdata)
        bdata.place(x = 130, y = 105, width = 100, height = 30)		

        
        ttk.Label(self.source_display_frame, text = "Data Parameter Settings:", font = ('Helvetica', 12), foreground = 'blue').place(x = 5, y = 160,  width = 240, height = 30)		
        
        ttk.Label(self.source_display_frame, text = "receive channels:").place(x = 5, y = 200,  width = 130, height = 30)		
        cchnum = ttk.Combobox(self.source_display_frame, textvariable = self.nchannel, state = 'readonly')
        cchnum['value'] = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
        cchnum.place(x = 140, y = 200 , width = 80, height = 30)
        cchnum.current(7)
#        cchnum.bind('<<ComboboxSelected>>', self.all_para)

        ttk.Label(self.source_display_frame, text = "send channels:").place(x = 5, y = 240,  width = 130, height = 30)		
        ttk.Entry(self.source_display_frame, textvariable = self.nline).place(x = 140, y = 240, width = 80, height = 30)

        ttk.Label(self.source_display_frame, text = "trigger sample number:").place(x = 5, y = 280,  width = 130, height = 30)		
        ttk.Entry(self.source_display_frame, textvariable = self.triggerlen).place(x = 140, y = 280, width = 80, height = 30)
   
        ttk.Label(self.source_display_frame, text = "point sample number:").place(x = 5, y = 320,  width = 130, height = 30)		
        ttk.Entry(self.source_display_frame, textvariable = self.pointsamplenum).place(x = 140, y = 320, width = 80, height = 30)
    
        ttk.Label(self.source_display_frame, text = "point valid number:").place(x = 5, y = 360,  width = 130, height = 30)		
        ttk.Entry(self.source_display_frame, textvariable = self.pvalidnum).place(x = 140, y = 360, width = 80, height = 30)

        ttk.Label(self.source_display_frame, text = "frame pause number:").place(x = 5, y = 400,  width = 130, height = 30)		
        ttk.Entry(self.source_display_frame, textvariable = self.framepausenum).place(x = 140, y = 400, width = 80, height = 30)

        ttk.Label(self.source_display_frame, text = "number of frames:").place(x = 5, y = 440,  width = 130, height = 30)		
        ttk.Entry(self.source_display_frame, textvariable = self.nframe).place(x = 140, y = 440, width = 80, height = 30)
    
        ttk.Label(self.source_display_frame, text = "data bits:").place(x = 5, y = 480,  width = 130, height = 30)		
        cdatabits = ttk.Combobox(self.source_display_frame, textvariable = self.bits, state = 'readonly')
        cdatabits['value'] = (10,12,14)
        cdatabits.place(x = 140, y = 480 , width = 80, height = 30)
        cdatabits.current(2)
        
        self.bcal = ttk.Button(self.source_display_frame, text = 'Convert and Plot', style = 'my.TButton', command = self.cal_convert_plot)
        self.bcal.place(x = 80, y = 520, width = 150, height = 30)
    
        #ttk.Label(self.source_display_frame, text = "Figure Plot Settings:", font = ('Helvetica', 12), foreground = 'blue').place(x = 5, y = 550,  width = 240, height = 30)		
        
        #ttk.Label(self.source_display_frame, text = "plot type:").place(x = 5, y = 590,  width = 80, height = 30)		
        #cplottype = ttk.Combobox(self.source_display_frame, textvariable = self.plottype, state = 'readonly')
        #cplottype['value'] = ('choose plot type', 'scatter', 'heatmap')
        #cplottype.place(x = 90, y = 590 , width = 130, height = 30)
        #cplottype.current(0)
        #cplottype.bind('<<ComboboxSelected>>', self.plotfigure)
    
    
    def create_frame_list_panel(self):
        list_display_frame = tk.Frame(self.root, height = 850 , width  = 120, relief = 'ridge', borderwidth = 1)
        list_display_frame.place(x = 265, y = 10, width = 120, height = 850)
        
        ttk.Label(list_display_frame, text = "Frame list:", font = ('Helvetica', 12), foreground = 'blue').place(x = 5, y = 5,  width = 110, height = 30)		
        self.edisplay = ScrolledText(master = list_display_frame, 
                                                     wrap =tk.WORD, font=("Helvetica", 10),
                                                     state = 'disabled')
        self.edisplay.place(x = 5, y = 40,  width = 110, height = 800)
        
        self.edisplay.bind('<Double-Button-1>', self.show_frame_plot)
        
    def create_frame_display_panel(self):
        self.figure_display_frame = tk.Frame(self.root, height = 850 , width  = 1180, relief = 'ridge', borderwidth = 1)
        self.figure_display_frame.place(x = 390, y = 10, width = 1180, height = 850)


    #===============================================================================
    def datafile_input(self): # get the datafile path and filename
        root = tk.Tk()
        root.withdraw()

        self.default_datafile = filedialog.askopenfilename(initialdir = '/', title = 'Select data file',
                                                     filetypes = (('csv files', '*.csv'),('all files', '*.*')))
        self.lsource['text'] = self.default_datafile
        
    def show_ADCdata(self):
        adc = tk.Toplevel(self.root)
        ADCdata(adc, self.default_datafile)
        
    def get_all_para(self):
        self.parameters = {'nchannel': self.nchannel.get(), 'nline': self.nline.get(), 'triggerlen': self.triggerlen.get(),
                           'pointsamplenum': self.pointsamplenum.get(), 'pvalidnum': self.pvalidnum.get(), 'framepausenum': self.framepausenum.get(),
                           'nframe': self.nframe.get(), 'databits': self.bits.get() }
        
        return self.parameters
    
    def cal_convert(self):
        setting = self.get_all_para()
        self.A = GratingSensor(self.default_datafile, **setting)
        
        self.plottype.set('choose plot type')
        
        self.edisplay.config(state = 'normal')
        self.edisplay.delete(1.0, 'end')
        self.edisplay.config(state = 'disabled')
        try:
#            self.frame_canvas_frame.winfo_exists():
            self.event_canvas_frame.destroy()
            self.event_toolbar_frame.destroy()
        except:
            print('No figure')

    def plotfigure(self, event):      
        self.framenumlist = self.A.PlotFrames(plottype = self.plottype.get())
        framelistname = [i for i in self.framenumlist]
        
        self.edisplay.config(state = 'normal')
        self.edisplay.delete(1.0, 'end')
        for k, i in enumerate(framelistname):
            self.edisplay.insert('{}.0'.format(k+1), i+'\n')
        self.edisplay.config(state = 'disabled')

        
        try:
#            self.frame_canvas_frame.winfo_exists():
            self.event_canvas_frame.destroy()
            self.event_toolbar_frame.destroy()
            
            self.embed_frame_plot(framelistname[0])

        except:
            self.embed_frame_plot(framelistname[0])

    def cal_convert_plot(self):
        setting = self.get_all_para()
        self.A = GratingSensor(self.default_datafile, **setting)

        self.framenumlist = self.A.PlotFrames(plottype = 'heatmap')
        framelistname = [i for i in self.framenumlist]
        
        self.edisplay.config(state = 'normal')
        self.edisplay.delete(1.0, 'end')
        for k, i in enumerate(framelistname):
            self.edisplay.insert('{}.0'.format(k+1), i+'\n')
        self.edisplay.config(state = 'disabled')

        try:
#            self.frame_canvas_frame.winfo_exists():
            self.event_canvas_frame.destroy()
            self.event_toolbar_frame.destroy()
            
            self.embed_frame_plot(framelistname[0])

        except:
            self.embed_frame_plot(framelistname[0])

    def show_frame_plot(self, event):
        #get frame name from the double click
        current_frame = self.edisplay.get("insert linestart", "insert lineend")
        
        try:
#            self.frame_canvas_frame.winfo_exists():
            self.event_canvas_frame.destroy()
            self.event_toolbar_frame.destroy()
            
            self.embed_frame_plot(current_frame)

        except:
            self.embed_frame_plot(current_frame)
    
    def embed_frame_plot(self, current_frame):
        
        #embed figure and toolbar
        self.event_canvas_frame = tk.Frame(self.figure_display_frame)
        self.event_canvas_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        canvas = FigureCanvasTkAgg(self.framenumlist[current_frame], master=self.event_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.event_toolbar_frame = tk.Frame(self.figure_display_frame)
        self.event_toolbar_frame.pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.event_toolbar_frame)
        toolbar.update()
    #=================================================================================
    
if __name__ == '__main__': main()