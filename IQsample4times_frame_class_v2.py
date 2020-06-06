
"""



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

        
        return [Imean, Qmean, Istd, Qstd]    
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
    
    

    

    def APsistatistic(self, A, psi):
        AA = A[~np.isnan(A)]
        Psi = psi[~np.isnan(psi)]
        Amean = np.mean(AA)
        psimean = np.mean(Psi)
        Astd = np.std(AA)
        psistd = np.std(Psi)

        
        return [Amean, psimean, Astd, psistd]
     
    def APsicalculation(self, I, Q):
        A = np.sqrt(I**2 + Q**2)
        psi = np.degrees(np.arctan(Q/I))
        
        return A, psi
       
    def PlotPoints(self, data, title):

        

        fQ = axs[0,1].scatter(x,y, s = 200, edgecolor = 'black', linewidths = 300*data[:,:,3].flatten(), c = data[:,:,1], cmap = cmap, norm = norm0)
        axs[0,1].set_title('Q_mean, Q_std', fontsize = 14)
        axs[0,1].tick_params(labelsize = 12, which = 'both')
        axs[0,1].grid()
        fig.colorbar(fQ, ax = axs[0,1], ticks = np.linspace(-2,2,21))
        
        fI = axs[0,0].scatter(x,y, s = 200, edgecolors = 'black', linewidths = 300*data[:,:,2].flatten(), c = data[:,:,0], cmap = cmap, norm = norm0)
        axs[0,0].set_title('I_mean, I_std', fontsize = 14)
        axs[0,0].set_ylabel('Send Channels', fontsize = 14)
        axs[0,0].tick_params(labelsize = 12, which = 'both')
        axs[0,0].xaxis.set_major_locator(ticker.MultipleLocator(1))
        axs[0,0].yaxis.set_major_locator(ticker.MultipleLocator(1))
        axs[0,0].grid()
        fig.colorbar(fI, ax = axs[0,0], ticks = np.linspace(-2,2,21))
        fig, axs = plt.subplots(2,2, sharex = True, sharey = True, figsize = (6.5,8))
        fig.subplots_adjust(top = 0.915, bottom = 0.06, left = 0.06, right = 0.995, hspace = 0.135, wspace = 0.01)
        x, y = np.meshgrid(np.arange(1,self.nchannel+1), np.arange(1,self.nline+1))
        axs[1,1].set_title('Psi_mean, Psi_std', fontsize = 14)
        axs[1,1].set_xlabel('Receive Channels', fontsize = 14)
        axs[1,1].tick_params(labelsize = 12, which = 'both')    
        axs[1,1].grid()    
        fA = axs[1,0].scatter(x,y, s = 200, edgecolor = 'black', linewidths = 300*data[:,:,6].flatten(), c = data[:,:,4], cmap = cmap, norm = norm)
        axs[1,0].set_title('A_mean, A_std', fontsize = 14)
        axs[1,0].set_xlabel('Receive Channels', fontsize = 14)
        axs[1,0].set_ylabel('Send Channels', fontsize = 14)
        axs[1,0].tick_params(labelsize = 12, which = 'both')
        axs[1,0].grid()
        fig.colorbar(fA, ax = axs[1,0], ticks = np.linspace(0,2,21))
        
        fP = axs[1,1].scatter(x,y, s = 200, edgecolor = 'black', linewidths = 90*data[:,:,7].flatten(), c = data[:,:,5], cmap = cmap1, norm = norm1)

        fig.colorbar(fP, ax = axs[1,1], ticks = np.linspace(0,90,19))
        
        fig.suptitle(title, fontsize = 18)
        plt.ioff()
        plt.close()
        return fig 
    
    def HeatmapPlot(self, data, title):

        axn[0,0] = sns.heatmap(data[:,:,4], linewidth = 0.1, annot = True, fmt = '.2f', 
                    vmin = 0, vmax = 2, xticklabels = xticklabels, yticklabels = yticklabels,
                    cmap = 'Reds', cbar = True, square = False, ax = axn[0,0],
                    cbar_kws = {'ticks': np.linspace(0,2,21), 'label': 'Amp.(V)'})
        axn[0,0].set_title('A_mean', fontsize = 14)
        axn[0,0].set_yticklabels(axn[0,0].get_yticklabels(), rotation=0, fontsize = 14)
        axn[0,0].set_ylabel('Send Channels', fontsize = 14)
        axn[0,0].invert_yaxis()

        axn[1,0].set_ylabel('Send Channels', fontsize = 14)
        axn[1,0].invert_yaxis()
        
        sns.heatmap(data[:,:,6]*1000, linewidth = 0.1, annot = True, fmt = '.1f', 
                    vmin = 0, vmax = 200, xticklabels = xticklabels, yticklabels = yticklabels,
                    cmap = 'Reds', cbar = True, square = False, ax = axn[1,0],
                    cbar_kws = {'ticks': np.linspace(0,200,11), 'label': 'Amp.(mV)'})

        sns.heatmap(data[:,:,5], linewidth = 0.1, annot = True, fmt = '.1f', 
                    vmin = 0, vmax = 90, xticklabels = xticklabels, yticklabels = yticklabels,
                    cmap = 'Reds', cbar = True, square = False, ax = axn[0,1],
                    cbar_kws = {'ticks': np.linspace(0,90,19),'label': 'Phase (deg.)'})
        axn[0,1].set_title('Psi_mean', fontsize = 14)
        axn[0,1].invert_yaxis()


        
if __name__ == '__main__': main()  