
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from HSDCPro_class import HSDCPro
from frame_viewer_v2 import FrameView
from ctypes import c_long, c_int, c_uint64, c_double
import math

def main():
    root = tk.Tk()
    MeasureView(root)
    root.mainloop()

class MeasureView():
    def __init__(self, root):
        self.root = root
        self.root.geometry("435x860+300+30")
        self.root.resizable(0,0)
        self.root.title('Grating Sensor Measure View')
        
        self.CSVFileFolderPath = ''
#        self.CSVFileName = 'data'
#        self.CSVFilePathWithName = os.path.join(self.CSVFileFolderPath, self.CSVFileName + '.csv')
        self.init_para()
        self.init_gui()
        
    def init_para(self):
        self.BoardSerialNumber = tk.StringVar()
        self.BoardSerialNumber.set('K1316284-TSW1400')
        self.ADCDevice = tk.StringVar()
        self.ADCDevice.set('ADS52J90')
        self.ADCOutputDataRate = tk.DoubleVar()

    def init_gui(self):
        
        s = ttk.Style()
        s.configure('my.TButton', font = ('Helvetica', 12), foreground = 'dark green')
        s.configure('my1.TButton', font = ('Helvetica', 12), foreground = 'purple')
        s.configure('my2.TButton', font = ('Helvetica', 12), foreground = 'red')
        s.configure('my3.TButton', font = ('Helvetica', 12), foreground = 'black')
        
        ttk.Label(self.root, text = "Measurement Settings:", font = ('Helvetica', 12,'bold'), foreground = 'blue').place(x = 10, y = 10,  width = 450, height = 30)		
        ttk.Label(self.root, text = "Samples Per Channel:").place(x = 50, y = 265,  width = 160, height = 30)       
#        ttk.Entry(self.root, textvariable = self.NumberOfSamplesPerChannel).place(x = 220, y = 230, width = 200, height = 30)
        cchnum = ttk.Combobox(self.root, textvariable = self.NumberOfSamplesPerChannel, state = 'readonly')
        cchnum['value'] = (4096,8192,12288,16384,20480,24576,28672,32768,36864,40960,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432)
        cchnum.place(x = 220, y = 265, width = 200, height = 30)
        cchnum.current(0)        
        ttk.Label(self.root, text = "Board Setting:", font = ('Helvetica', 10, 'bold')).place(x = 10, y = 50,  width = 200, height = 30)		
        ttk.Label(self.root, text = "Board Serial Number:").place(x = 50, y = 85,  width = 160, height = 30)		
        ttk.Entry(self.root, textvariable = self.BoardSerialNumber).place(x = 220, y = 85, width = 200, height = 30)

        ttk.Label(self.root, text = "ADC Device:").place(x = 50, y = 120,  width = 160, height = 30)		
        ttk.Entry(self.root, textvariable = self.ADCDevice).place(x = 220, y = 120, width = 200, height = 30)
        
        ttk.Label(self.root, text = "Configuration Setting:", font = ('Helvetica', 10, 'bold')).place(x = 10, y = 160,  width = 200, height = 30)		
        ttk.Label(self.root, text = "ADC Output Data Rate:").place(x = 50, y = 195,  width = 160, height = 30)		
        ttk.Entry(self.root, textvariable = self.ADCOutputDataRate).place(x = 220, y = 195, width = 150, height = 30)
        ttk.Label(self.root, text = "MHz").place(x = 380, y = 195,  width = 50, height = 30)		


        ttk.Label(self.root, text = "Trigger Mode Enable:").place(x = 50, y = 300,  width = 160, height = 30)		
#        ttk.Entry(self.root, textvariable = self.TriggerModeEnable).place(x = 220, y = 270, width = 200, height = 30)
        ctrigger = ttk.Combobox(self.root, textvariable = self.TriggerModeEnable, state = 'readonly')
        ctrigger['value'] = (1,0)
        ctrigger.place(x = 220, y = 300, width = 200, height = 30)
        ctrigger.current(0)
        
        ttk.Label(self.root, text = "Measure Process:", font = ('Helvetica', 12, 'bold'), foreground = 'blue').place(x = 10, y = 345,  width = 450, height = 30)		
        
        self.bpre = ttk.Button(self.root, text = 'Preparation', style = 'my.TButton', command = self.Preparation)
        self.bpre.place(x = 155, y = 385, width = 115, height = 30)        photo = tk.PhotoImage(file = 'bitmap2.png')
        w = ttk.Label(self.root, image = photo)
        w.photo = photo
        self.bcon = ttk.Button(self.root, text = 'Configuration', style = 'my.TButton', state = 'disabled', command = self.Configuration)
        self.bcon.place(x = 120, y = 475, width = 150, height = 30)

        self.bfolder = ttk.Button(self.root, text = 'Data Folder', style = 'my3.TButton', command = self.Data_folder)
        self.bfolder.place(x = 10, y = 520, width = 100, height = 30)        
        self.lfolder = ttk.Label(self.root, text = self.CSVFileFolderPath, background = "white", wraplength = 300)
        self.lfolder.place(x = 115, y = 520, width = 300, height = 30)

        ttk.Label(self.root, text = "File Name:", font = ('Helvetica', 12)).place(x = 20, y = 560,  width = 90, height = 30)		
        self.Efile = ttk.Entry(self.root, textvariable = self.CSVFileName)
        self.Efile.place(x = 115, y = 560, width = 300, height = 30)
        
        self.bcapture = ttk.Button(self.root, text = 'Capture Data', style = 'my.TButton', state = 'disabled', command = self.Data_Capture)
        self.bcapture.place(x = 120, y = 605, width = 150, height = 30)

        self.bdiscon = ttk.Button(self.root, text = 'Disconnect Device', style = 'my.TButton', state = 'disabled', command = self.Disconnect_Device)
        self.bdiscon.place(x = 120, y = 650, width = 150, height = 30)



        ttk.Label(self.root, text = "Data Analyse:", font = ('Helvetica', 12, 'bold'), foreground = 'blue').place(x = 10, y = 720,  width = 115, height = 30)		
        self.banalyse = ttk.Button(self.root, text = 'Data Analyse', style = 'my1.TButton', command = self.Data_Analyse)
        self.banalyse.place(x = 130, y = 720, width = 150, height = 35)


        ttk.Label(self.root, text = "Quit GUI:", font = ('Helvetica', 12, 'bold'), foreground = 'blue').place(x = 10, y = 790,  width = 115, height = 30)		
        ttk.Button(self.root, text = 'Quit GUI', style = 'my2.TButton',  command = self.Quit_Gui).place(x = 130, y = 790, width = 150, height = 35)
        
    def Preparation(self):
        checkm = messagebox.askyesno(title = 'Preparation finished?', 
                            message = ' 1. Hardware Connected? \n 2.HSDCPro GUI Opened? \n 3. No pop up dialogs in HSDCPro GUI? \n 4. Measurement Setting are Correct?')
        if checkm:
            self.bset['state'] = 'normal'
            
    def get_all_para(self):
        self.parameters = {'BoardSerialNumber': self.BoardSerialNumber.get(), 'ADCDevice': self.ADCDevice.get()}
        
#        'ADCOutputDataRate': self.ADCOutputDataRate.get()*1000000, 'ADCInputTargetFrequency': self.ADCInputTargetFrequency.get()*1000000,
#                           'NumberOfSamplesPerChannel': self.NumberOfSamplesPerChannel.get(), 'TriggerModeEnable': self.TriggerModeEnable.get()
        
        return self.parameters

    def Connect_Device(self):
        setting = self.get_all_para()
        self.A = HSDCPro(**setting)
        self.A.Connect_Board()
        self.A.Select_ADC_Device()
        self.A.HSDC_Ready()
#        messagebox.showinfo(title = 'HMC-DAQ GUI Setup', message = 'Please MANUALLY Setup HMC-DAQ GUI\nTHEN Press ENTER to Continue')
        self.A.Manual_Setup_HMC_DAQ_GUI()
        self.bcon['state'] = 'normal'
        self.bdiscon['state'] = 'normal'
        self.bset['state'] = 'disabled'
        
    def Configuration(self):
        self.A.Pass_ADC_Output_Data_Rate(c_double(self.ADCOutputDataRate.get()*1000000))
        self.A.Set_ADC_Input_Target_Frequency(c_double(self.ADCInputTargetFrequency.get()*1000000))
        self.A.Set_Number_of_Samples(c_uint64(self.NumberOfSamplesPerChannel.get()))
        self.A.Trigger_Option(c_int(self.TriggerModeEnable.get()))
#        self.bfolder['state'] = 'normal'
#        self.Efile['state'] = 'normal'
    
    def Data_folder(self):
        root = tk.Tk()
        root.withdraw()

        self.CSVFileFolderPath = filedialog.askdirectory(initialdir = '/', title = 'Choose Data Saving Folder')
        self.lfolder['text'] = self.CSVFileFolderPath
        self.bcapture['state'] = 'normal'
        
    def get_csvsavefile(self):
        return os.path.join(self.CSVFileFolderPath, self.CSVFileName.get() + '.csv')

    def Data_Capture(self):
        self.CSVFilePathWithName = self.get_csvsavefile()
        
        sn = self.NumberOfSamplesPerChannel.get()
        if sn > 65536:
            TimeoutInMs1 = c_long(math.ceil(sn/65536)*30000)
            TimeoutInMs2 = c_long(math.ceil(sn/65536)*60000)
        else:
            TimeoutInMs1 = c_long(30000)
            TimeoutInMs2 = c_long(60000)
            
        if self.TriggerModeEnable:
            self.A.Read_DDR_Memory(TimeoutInMs1)
        else:
            self.A.Pass_Capture_Event(TimeoutInMs1)
        self.A.HSDC_Ready()
        self.A.Save_Raw_Data_As_CSV(self.CSVFilePathWithName.encode('ascii'), TimeoutInMs2)
#        self.banalyse['state'] = 'normal'
        
    def Disconnect_Device(self):
        self.A.Disconnect_Board()
        self.bset['state'] = 'normal'
        
    def Data_Analyse(self):
        self.CSVFilePathWithName = self.get_csvsavefile()
        Aframe = tk.Toplevel(self.root)
        self.B = FrameView(Aframe, self.CSVFilePathWithName)
        
    def Quit_Gui(self):
        self.root.destroy()
if __name__ == '__main__': main()