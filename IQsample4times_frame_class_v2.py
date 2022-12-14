
"""


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
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import numpy as np
import seaborn as sns

def main():
    f = 'ADSdata_20.csv'
    setting = dict(nframe=1, nline = 2, nchannel = 2, pointsamplenum = 1)
    A = GratingSensor(f, **setting)
    A.ShowFigures()

class GratingSensor():
    def __init__(self, f, **kwargs):
        self.f = f
        self.nchannel = kwargs.get('nchannel', 8)
        self.nline = kwargs.get('nline', 8)
        self.pointsamplenum = kwargs.get('pointsamplenum', 160)
        self.pvalidnum = kwargs.get('pvalidnum', 100)
        self.nframe = kwargs.get('nframe', 3)
        self.triggerlen = kwargs.get('triggerlen', 20)
        self.databits = kwargs.get('databits', 14)
        self.framepausenum = kwargs.get('framepausenum', 688)
        
        self.defaultsendchn = 8
        self.framesamplenum = self.pointsamplenum*self.defaultsendchn+self.framepausenum
        self.chvalidlen = self.framesamplenum*self.nframe
        
###=============================================================================###                 
                    # cited functions   
###=============================================================================### 
# calculation A, Psi    
    def IQsample4times(self): # nframe: number of frames
        list_of_dfs = self.ReadSplitFile()
        cdata = np.zeros((self.nline*self.nframe, self.nchannel, 8))
        for i, v in enumerate(list_of_dfs):
            for j, col in enumerate(v.columns):
                I, Q = self.IQcalculation(np.array(v[col]))
                cdata[i,j,0:4] = self.IQstatistic(I,Q)
#                print('I', cdata[i,j,0])
#                print('Q', cdata[i,j,1])

                A, Psi = self.APsicalculation(I, Q)
#                print('i, j', i, j)
#                print('A', A)
#                print('Psi', Psi)
                cdata[i,j,4:8] = self.APsistatistic(A, Psi)
#                print('A', cdata[i,j,4])
#                print('Psi', cdata[i,j,5])
        return cdata  
    
    # plot frames
    def PlotFrames(self, plottype = 'heatmap'): #split the calculated data into 8*8*8 3d numpy array, plot respectively and store in a dict with name in sequence 'Frame_i'
        cdata = self.IQsample4times()
        list_of_cdatas = [cdata[i*self.nline:(i+1)*self.nline, :, :] for i in range(self.nframe)]
        figdict = dict()
        for i, v in enumerate(list_of_cdatas):
            if plottype == 'scatter':
                figdict['FrameS_'+str(i+1)] = self.PlotPoints(v, 'FrameS_'+str(i+1))
            elif plottype == 'heatmap':
                figdict['FrameH_'+str(i+1)] = self.HeatmapPlot(v, 'FrameH_'+str(i+1))
        return figdict
    
    #show figures
    def ShowFigures(self): # show all the frame figures
        ff = self.PlotFrames()
        for v in ff.values():
            v.show()
        
    ###=============================================================================###                 
                        # private functions   
    ###=============================================================================###  
    def ReadSplitFile(self):
        df = pd.read_csv(self.f, header = None, skiprows = self.triggerlen)
        df.columns = ['ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','ch13','ch14','ch15','ch16']
        nd = self.nchannel
        df.drop(df.iloc[:,nd:16], inplace = True, axis = 1) # drop the unused 8 channels: ch9 to ch16
        
        list_of_dfs0 = [df.loc[i: i+self.framesamplenum-1,:] for i in range(0, self.chvalidlen, self.framesamplenum)] # split df into smaller dataframe with a length of 160*8+688 samples

        list_of_dfs = [dff.reset_index(drop = True).loc[i: i+self.pointsamplenum-1,:] for dff in list_of_dfs0 for i in range(0, self.pointsamplenum*self.nline, self.pointsamplenum)] # select only the dataframe for sending signal channels

        return list_of_dfs
    
    def ToVolt(self):
        voltfactor = {'10': 251.4, '12': 1005, '14':4020}
        
        return voltfactor[str(self.databits)]
    
    def IQcalculation(self, dd): # num: valid number of samples for 1 grill point stype=1 -> 120, stype = 2 -> 240
        a = []
        b = []
        factor = self.ToVolt()
        d = dd/factor
#        print('factor', factor)
#        print('d',dd)
        for i, v in enumerate(d):
            if i < self.pvalidnum-2:
                a0 = np.cos(i*np.pi/2)*d[i+1] - np.cos((i+1)*np.pi/2)*d[i]
                b0 = -np.sin(i*np.pi/2)*d[i+1] + np.sin((i+1)*np.pi/2)*d[i]
                a.append(a0)
                b.append(b0)
      
        return np.array(a), np.array(b)
    
    
    def IQstatistic(self, I,Q):
        Imean = np.mean(I)
        Qmean = np.mean(Q)
        Istd = np.std(I)
        Qstd = np.std(Q)
        
        return [Imean, Qmean, Istd, Qstd]
    
    
    def APsicalculation(self, I, Q):
        A = np.sqrt(I**2 + Q**2)
        psi = np.degrees(np.arctan(Q/I))
        
        return A, psi
    
    def APsistatistic(self, A, psi):
        AA = A[~np.isnan(A)]
        Psi = psi[~np.isnan(psi)]
        Amean = np.mean(AA)
        psimean = np.mean(Psi)
        Astd = np.std(AA)
        psistd = np.std(Psi)
        
        if psimean < 0:
            psimean = psimean + 90
        
        return [Amean, psimean, Astd, psistd]
    
    def PlotPoints(self, data, title):
        cmap = plt.cm.get_cmap('jet')
        cmap1 = plt.cm.get_cmap('jet')
        norm = mpl.colors.BoundaryNorm(np.arange(-0.05,2.15,0.1), cmap.N)
        norm0 = mpl.colors.BoundaryNorm(np.arange(-2.1,2.3,0.2), cmap.N)
        norm1 = mpl.colors.BoundaryNorm(np.arange(-2.5,97.5,5), cmap1.N)

        
        fig, axs = plt.subplots(2,2, sharex = True, sharey = True, figsize = (6.5,8))
        fig.subplots_adjust(top = 0.915, bottom = 0.06, left = 0.06, right = 0.995, hspace = 0.135, wspace = 0.01)
        x, y = np.meshgrid(np.arange(1,self.nchannel+1), np.arange(1,self.nline+1))

        fI = axs[0,0].scatter(x,y, s = 200, edgecolors = 'black', linewidths = 300*data[:,:,2].flatten(), c = data[:,:,0], cmap = cmap, norm = norm0)
        axs[0,0].set_title('I_mean, I_std', fontsize = 14)
        axs[0,0].set_ylabel('Send Channels', fontsize = 14)
        axs[0,0].tick_params(labelsize = 12, which = 'both')
        axs[0,0].xaxis.set_major_locator(ticker.MultipleLocator(1))
        axs[0,0].yaxis.set_major_locator(ticker.MultipleLocator(1))
        axs[0,0].grid()
        fig.colorbar(fI, ax = axs[0,0], ticks = np.linspace(-2,2,21))
    
        fQ = axs[0,1].scatter(x,y, s = 200, edgecolor = 'black', linewidths = 300*data[:,:,3].flatten(), c = data[:,:,1], cmap = cmap, norm = norm0)
        axs[0,1].set_title('Q_mean, Q_std', fontsize = 14)
        axs[0,1].tick_params(labelsize = 12, which = 'both')
        axs[0,1].grid()
        fig.colorbar(fQ, ax = axs[0,1], ticks = np.linspace(-2,2,21))
        
        fA = axs[1,0].scatter(x,y, s = 200, edgecolor = 'black', linewidths = 300*data[:,:,6].flatten(), c = data[:,:,4], cmap = cmap, norm = norm)
        axs[1,0].set_title('A_mean, A_std', fontsize = 14)
        axs[1,0].set_xlabel('Receive Channels', fontsize = 14)
        axs[1,0].set_ylabel('Send Channels', fontsize = 14)
        axs[1,0].tick_params(labelsize = 12, which = 'both')
        axs[1,0].grid()
        fig.colorbar(fA, ax = axs[1,0], ticks = np.linspace(0,2,21))
        
        fP = axs[1,1].scatter(x,y, s = 200, edgecolor = 'black', linewidths = 90*data[:,:,7].flatten(), c = data[:,:,5], cmap = cmap1, norm = norm1)
        axs[1,1].set_title('Psi_mean, Psi_std', fontsize = 14)
        axs[1,1].set_xlabel('Receive Channels', fontsize = 14)
        axs[1,1].tick_params(labelsize = 12, which = 'both')    
        axs[1,1].grid()
        fig.colorbar(fP, ax = axs[1,1], ticks = np.linspace(0,90,19))
        
        fig.suptitle(title, fontsize = 18)
        plt.ioff()
        plt.close()
        return fig 
    
    def HeatmapPlot(self, data, title):
        fig, axn = plt.subplots(2, 2, sharex = True, sharey = True, figsize = (6.5,8))
        fig.subplots_adjust(top = 0.915, bottom = 0.06, left = 0.06, right = 0.995, hspace = 0.135, wspace = 0.01)
        xticklabels = range(1,self.nchannel+1)
        yticklabels = range(1,self.nline+1)
        axn[0,0] = sns.heatmap(data[:,:,4], linewidth = 0.1, annot = True, fmt = '.2f', 
                    vmin = 0, vmax = 2, xticklabels = xticklabels, yticklabels = yticklabels,
                    cmap = 'Reds', cbar = True, square = False, ax = axn[0,0],
                    cbar_kws = {'ticks': np.linspace(0,2,21), 'label': 'Amp.(V)'})
        axn[0,0].set_title('A_mean', fontsize = 14)
        axn[0,0].set_yticklabels(axn[0,0].get_yticklabels(), rotation=0, fontsize = 14)
        axn[0,0].set_ylabel('Send Channels', fontsize = 14)
        axn[0,0].invert_yaxis()
        
        sns.heatmap(data[:,:,6]*1000, linewidth = 0.1, annot = True, fmt = '.1f', 
                    vmin = 0, vmax = 200, xticklabels = xticklabels, yticklabels = yticklabels,
                    cmap = 'Reds', cbar = True, square = False, ax = axn[1,0],
                    cbar_kws = {'ticks': np.linspace(0,200,11), 'label': 'Amp.(mV)'})
        axn[1,0].set_title('A_std', fontsize = 14)
        axn[1,0].set_xticklabels(axn[1,0].get_xticklabels(), fontsize = 14)        
        axn[1,0].set_yticklabels(axn[1,0].get_yticklabels(), rotation=0, fontsize = 14)
        axn[1,0].set_xlabel('Receive Channels', fontsize = 14)
        axn[1,0].set_ylabel('Send Channels', fontsize = 14)
        axn[1,0].invert_yaxis()

        sns.heatmap(data[:,:,5], linewidth = 0.1, annot = True, fmt = '.1f', 
                    vmin = 0, vmax = 90, xticklabels = xticklabels, yticklabels = yticklabels,
                    cmap = 'Reds', cbar = True, square = False, ax = axn[0,1],
                    cbar_kws = {'ticks': np.linspace(0,90,19),'label': 'Phase (deg.)'})
        axn[0,1].set_title('Psi_mean', fontsize = 14)
        axn[0,1].invert_yaxis()

        sns.heatmap(data[:,:,7], linewidth = 0.1, annot = True, fmt = '.1f', 
                    vmin = 0, vmax = 90, xticklabels = xticklabels, yticklabels = yticklabels,
                    cmap = 'Reds', cbar = True, square = False, ax = axn[1,1],
                    cbar_kws = {'ticks': np.linspace(0,90,11), 'label': 'Phase (deg.)'})
        axn[1,1].set_title('Psi_std', fontsize = 14)
        axn[1,1].set_xticklabels(axn[1,1].get_xticklabels(), fontsize = 14)
        axn[1,1].set_xlabel('Receive Channels', fontsize = 14)
        axn[1,1].invert_yaxis()
        
        fig.suptitle(title, fontsize = 18)
        plt.ioff()
        plt.close()
        return fig 
        
if __name__ == '__main__': main()  