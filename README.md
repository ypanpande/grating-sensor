# Evaluation board control, data collection and analysis
A tool to customisely control of evaluation board (ADS52J90), to collect the measured data and process the data. The visualization is auch included.



## Overview
This software is for customized controling of evaluation board (ADS52J90) to collect the measured data from grating sensor. The collected data are processed and analyzed in order to detect the ratio between gas and water/oil. It is a convenient and straightforward application with advanced features.  

### Screenshots

<div align = "center">
  <img align = "center" width = "600" src = "/assets/image1.jpg">
<p align = "center">Overview of evaluation board</p> <br>
    <img align = "center" width = "600" src = "/assets/image2.jpg"/>
        <p align = "center"> Data process and visualizaiton</p><br>     
</div>

### How to use

grating structure: 8channels*8lines = 64 points
reference frequency: 20MHz
signal frequency: 5MHz

input signal period: 
stype = 1: 6us (signal) + 2us (pause) = 8us 
           number of samples for 1 point is 8us*20MHz = 160 samples, one channel for one frame has samples 160*8 = 1280
stype = 2: 12us (signal) + 4us (pause) = 16us 
           number of samples for 1 point is 16us*20MHz = 320 samples, one channel for one frame has samples 320*8 = 2560

for 1 channel the minimum recorded samples is 4096, number of frames for stype = 1 is 3, for stype = 2 is 1
maximum recorded samples is 1024 MB(=1GB)/2bytes/16channels = 32 Msamples = 32768 Ksamples = 33554432 samples

grating structure: number of channel (nchannel)*number of line (nline)
reference frequency: 20MHz
signal frequency: 5MHz

input signal period: for example, 6us (signal) + 2us (pause) = 8us
                     number of samples for 1 point is 8us*20MHz = 160 samples, that is the sample number (pointsamplenum),
                     one channel for one frame has samples pointsamplenum*nline, that is, the valid data length of datafile of one channel is pointsamplenum*16*nframe (chvalidlen)
                     number of samples of 1 point used for analysing signal is 6us*20MHz = 120 samples, that is valid number (pvalidnum)

class GratingSensor: 
    input parameters:
        nchannel: number of channels to receive signal, default value: 8
        nline: number of lines to send signal, default value: 8
        pointsamplenum: number of samples for 1 point, default value: 160
        pvalidnum: number of valid samples for 1 point, default value: 100
        nframe: number of frames for the whole datafile, default value:3
        triggerlen: number of samples for trigger signal, default value:20
        databits: selected data format of ADS52J90 board, default value: 14 
    cited functions:
        IQsample4times(): calculate the mean and std value of I, Q, A, Psi for all points 
                                    of grating structure recorded in the datafile
                          output is a 3d numpy array, x has number of 16*nframe, y is nchannal, 
                                    z is Imean, Qmean, Istd, Qstd, Amean, Psimean, Astd, Psistd in sequence
        PlotFrames(): scatter plot the calculated data resulting from IQsample4times in frames, store in dict with name in sequence 'Frame_i'
                      the edgewidth of scatterpoint is the value of std
                      the color of scatterpoint is the value of mean
        ShowFigures(): display the figure of the frames
        

## Python dependencies
The list of required python packages is contained in the [requirements.txt](requirements.txt) file in this repository. After install the required dependencies, run `main_EDS_composition.py` to execute the program.