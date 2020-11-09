#!/usr/bin/env python


import os
#import sys
#import win32api

from ctypes import cdll, byref, c_ulong, c_long, c_int, c_uint, c_uint64, c_ushort, c_double, c_char_p, c_ubyte, create_string_buffer



class HSDCPro:
    def __init__(self, **kwargs):
        
        #'''************************************************************************************************************************'''#
        #'''******************************** Loading the HSDCPro Automation DLL ****************************************************'''#
        #'''************************************************************************************************************************'''#

        if('PROGRAMFILES(X86)' in os.environ): #selecting the DLL path from HSDC Pro installed location based on 32 bit or 64 bit OS
            dll_path = "C:\\Program Files (x86)\\Texas Instruments\\High Speed Data Converter Pro\\HSDCPro Automation DLL\\64Bit DLL\\HSDCProAutomation_64Bit.dll"
        else:
            dll_path = "C:\\Program Files\\Texas Instruments\\High Speed Data Converter Pro\\HSDCPro Automation DLL\\64Bit DLL\\HSDCProAutomation_64Bit.dll"
        
        self.hsdcdll = cdll.LoadLibrary(dll_path)
        
        #'''*************************************************************************************************************************'''#
        #'''***************************************ADC Configuration Settings********************************************************'''#
        #'''*************************************************************************************************************************'''#
        
        # set Board Serial Number, ADC device, Configuration Settings, Trigger Settings, File Save Settings
        self.BoardSerialNumber = kwargs.get('BoardSerialNumber', 'K1316284-TSW1400').encode('ascii')
        self.ADCDevice = kwargs.get('ADCDevice', 'ADS52J90').encode('ascii')
        
#        self.ADCOutputDataRate = c_double(kwargs.get('ADCOutputDataRate', 20000000))
#        self.ADCInputTargetFrequency = c_double(kwargs.get('ADCInputTargetFrequency', 5000000))
#        self.NumberOfSamplesPerChannel = c_uint64(kwargs.get('NumberOfSamplesPerChannel', 4096))
        
#        self.TriggerModeEnable = c_int(kwargs.get('TriggerModeEnable', 1))
        self.SoftwareTriggerEnable = c_int(kwargs.get('SoftwareTriggerEnable', 0))
        self.ArmOnNextCaptureButtonPress = c_int(kwargs.get('ArmOnNextCaptureButtonPress', 0))
        self.TriggerCLKDelays = c_int(kwargs.get('TriggerCLKDelays', 0))
        self.WaitToCheckTrigger = c_int(kwargs.get('WaitToCheckTrigger', 1))
        
#        self.CSVFileFolderPath = kwargs.get('CSVFileFolderPath', 'C:\\Users\\Teletronic\\Desktop\\Neuer Ordner\\ADS52J90\\IQsample4time_auto')
#        self.CSVFileName = kwargs.get('CSVFileName', 'data')
#        self.CSVFilePathWithName = os.path.join(self.CSVFileFolderPath, self.CSVFileName + '.csv').encode('ascii')
        
        self.TimeoutInMs = c_long(30000)
        
    #'''*************************************************************************************************************************'''#    
    #'''**************************** The actual call to the function contained in the dll ***************************************'''#
    #'''*************************************************************************************************************************'''#
    
    #  Connecting to the board      
    def Connect_Board(self):
        try:
            print('Connect_Board: START')
            status = self.hsdcdll.Connect_Board(self.BoardSerialNumber,self.TimeoutInMs)
            print('Connect_Board: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Connect_Board: FAIL, status = '+str(status)+'\n')
            
    # selecting ADC device             
    def Select_ADC_Device(self):
        try:
            print('Select_ADC_Device: START')
            status = self.hsdcdll.Select_ADC_Device(self.ADCDevice, c_long(120000))
            print('Select_ADC_Device: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Select_ADC_Device: FAIL, status = '+str(status)+'\n')
            
    # Manually Setup HMC-DAQ GUI, then continue the process     
    def Manual_Setup_HMC_DAQ_GUI(self):
        print('Please Manually Set up HMC-DAQ GUI !!! ')
        input('Please Press ENTER to continue')   
        
        
    # Check that HSDC Pro is Ready
    def HSDC_Ready(self):
        try:
            print('HSDC_Ready: START')
            status = self.hsdcdll.HSDC_Ready(c_long(60000))
            print('HSDC_Ready: COMPLETE, status = '+str(status)+'\n')
        except:
            print('HSDC_Ready: FAIL, status = '+str(status)+'\n')
     
    # Set the Sampling rate in HSDC Pro
    def Pass_ADC_Output_Data_Rate(self, ADCOutputDataRate  = c_double(20000000)):
        try:
            print('Pass_ADC_Output_Data_Rate: START')
            status = self.hsdcdll.Pass_ADC_Output_Data_Rate(ADCOutputDataRate, self.TimeoutInMs)
            print('Pass_ADC_Output_Data_Rate: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Pass_ADC_Output_Data_Rate: FAIL, status = '+str(status)+'\n')
        
    # Set the ADC Input Target Frequency in HSDC Pro
    def Set_ADC_Input_Target_Frequency(self, ADCInputTargetFrequency = c_double(5000000)):
        try:
            print('Set_ADC_Input_Target_Frequency: START')
            status = self.hsdcdll.Set_ADC_Input_Target_Frequency(ADCInputTargetFrequency, self.TimeoutInMs)
            print('Set_ADC_Input_Target_Frequency: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Set_ADC_Input_Target_Frequency: FAIL, status = '+str(status)+'\n')
        
        
    # Set the Number of Samples/capture in HSDC Pro
    def Set_Number_of_Samples(self, NumberOfSamplesPerChannel = c_uint64(4096)):
        try:
            print('Set_Number_of_Samples per Channel: START')
            status = self.hsdcdll.Set_Number_of_Samples(NumberOfSamplesPerChannel,self.TimeoutInMs)
            print('Set_Number_of_Samples per Channel: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Set_Number_of_Samples per Channel: FAIL, status = '+str(status)+'\n')
        
    # Applying Trigger Settings in HSDC Pro
    def Trigger_Option(self, TriggerModeEnable = c_int(0)):
        try:
            print('Applying Trigger Settings: START')
            status = self.hsdcdll.Trigger_Option(TriggerModeEnable,self.SoftwareTriggerEnable,self.ArmOnNextCaptureButtonPress,self.TriggerCLKDelays,self.TimeoutInMs)
            print('Applying Trigger Settings: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Applying Trigger Settings: FAIL, status = '+str(status)+'\n')
        
    # Capture Data
    def Pass_Capture_Event(self, TimeoutInMs = c_long(30000)):
        try:
            print('Pass_Capture_Event: START')
            status = self.hsdcdll.Pass_Capture_Event(TimeoutInMs)
            print('Pass_Capture_Event: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Pass_Capture_Event: FAIL, status = '+str(status)+'\n')
        
    #Reading DDR Memory
    def Read_DDR_Memory(self, TimeoutInMs = c_long(30000)):
        try:
            print('Read_DDR_Memory: START')
            status = self.hsdcdll.Read_DDR_Memory(self.WaitToCheckTrigger, TimeoutInMs)
            print('Read_DDR_Memory: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Read_DDR_Memory: FAIL, status = '+str(status)+'\n')
        
        
    # Save Data to a csv file
    def Save_Raw_Data_As_CSV(self, CSVFilePathWithName, TimeoutInMs = c_long(60000)):
        try:
            print('Save_Raw_Data_As_CSV: START')
            status = self.hsdcdll.Save_Raw_Data_As_CSV(CSVFilePathWithName,TimeoutInMs)
            print('Save_Raw_Data_As_CSV: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Save_Raw_Data_As_CSV: FAIL, status = '+str(status)+'\n')

    # Dosconnect from the board
    def Disconnect_Board(self):
        try:
            print('Disconnect_Board: START')
            status = self.hsdcdll.Disconnect_Board(c_long(60000))
            print('Disconnect_Board: COMPLETE, status = '+str(status)+'\n')
        except:
            print('Disconnect_Board: FAIL, status = '+str(status)+'\n')
        


#if __name__ == '__main__': main()


