from PyQt5 import QtWidgets,QtCore,QtGui,QtMultimedia
from mainwindow import Ui_MainWindow
from window import Ui_MainWindow1
from compare import Ui_MainWindow2
import math
import pyqtgraph as pg
import sys,os
from scipy.io import wavfile
from scipy.fftpack import fft,rfft
import numpy as np
import pandas as pd
QMediaPlayer=QtMultimedia.QMediaPlayer
QMediaContent=QtMultimedia.QMediaContent
QAction=QtWidgets.QAction


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.diff = Ui_MainWindow1()
        self.comp = Ui_MainWindow2()
        self.compareWindow = QtWidgets.QMainWindow()
        self.diffWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self)
        self.comp.setup2(self.compareWindow)  
        self.diff.setup(self.diffWindow)  
        self.i = 0
        self.player = QMediaPlayer(self)
        self.player1 = QMediaPlayer(self) 
        self.player2 = QMediaPlayer(self)
        self.mediaplayers=[self.player,self.player1,self.player2]
        self.progressbars = [self.ui.progressBar,self.comp.mediaplayer1,self.comp.mediaplayer2]
        # self.message = [self.ui.statusBar,self.comp.statusbar]
        self.fileName= ["F:/eq/data.wav" , "F:/eq/comp1.wav","F:/eq/comp2.wav"]
        self.plays = [self.ui.play,self.comp.Play1,self.comp.play2] 
        self.pauses = [self.ui.pause,self.comp.pause1,self.comp.pause2]
        self.stops = [self.ui.stop,self.comp.stop1,self.comp.stop2]
        self.ui.save.clicked.connect(self.save_file)

        self.pauses[0].clicked.connect(self.mediaplayers[0].pause)
        self.plays[0].clicked.connect(self.mediaplayers[0].play)
        self.stops[0].clicked.connect(self.mediaplayers[0].stop)
        self.mediaplayers[0].durationChanged.connect(self.update_duration)
        self.mediaplayers[0].positionChanged.connect(self.update_position)
        self.pauses[1].clicked.connect(self.mediaplayers[1].pause)
        self.plays[1].clicked.connect(self.mediaplayers[1].play)
        self.stops[1].clicked.connect(self.mediaplayers[1].stop)
        self.mediaplayers[1].durationChanged.connect(self.update_duration1)
        self.mediaplayers[1].positionChanged.connect(self.update_position1)
        self.pauses[2].clicked.connect(self.mediaplayers[2].pause)
        self.plays[2].clicked.connect(self.mediaplayers[2].play)
        self.stops[2].clicked.connect(self.mediaplayers[2].stop)
        self.mediaplayers[2].durationChanged.connect(self.update_duration2)
        self.mediaplayers[2].positionChanged.connect(self.update_position2)
        # for i in range(len(self.mediaplayers)):
        #     self.i=i
        #     self.pauses[i].clicked.connect(self.mediaplayers[i].pause)
        #     self.plays[i].clicked.connect(self.mediaplayers[i].play)
        #     self.stops[i].clicked.connect(self.mediaplayers[i].stop)
        #     self.mediaplayers[i].durationChanged.connect(self.update_duration)
        #     self.mediaplayers[i].positionChanged.connect(self.update_position)
        self.datafft = np.array([])
        self.absfftdata= np.array([])
        self.ui.browser.clicked.connect(self.getfiles)
        self.ui.results.activated.connect(self.change) 
        self.sliders = [self.ui.slider1,self.ui.slider2,self.ui.slider3,self.ui.slider4,self.ui.slider5,self.ui.slider6,self.ui.slider7,self.ui.slider8,self.ui.slider9,self.ui.slider10]
        self.texts=[self.ui.Gain_Band1,self.ui.Gain_Band2,self.ui.Gain_Band3,self.ui.Gain_Band4,self.ui.Gain_Band5,self.ui.Gain_Band6,self.ui.Gain_Band7,self.ui.Gain_Band8,self.ui.Gain_Band9,self.ui.Gain_Band10]
        self.graphsTime = [self.ui.OriginalData_Time,self.ui.DataAfterEdit_Time,self.comp.Compare1TimeDomain,self.comp.Compare2TimeDomain,self.diff.DiffTime]
        self.graphsFreq = [self.ui.OriginalData_Freq,self.ui.DataAfterEdit_Freq,self.comp.Compare1FreqDomain,self.comp.Compare2FreqDomain,self.diff.DiffFreq]
        self.compare2 =[self.comp.Compare2FreqDomain,self.comp.Compare2TimeDomain,self.comp.play2,self.comp.pause2,self.comp.stop2,self.comp.mediaplayer2]
        self.compareflag = 0
        self.numBands=20
        self.numSliders=10
        for i in range(self.numSliders):
            self.texts[i].setText("1")
            self.sliders[i].valueChanged.connect(self.Gain)
    
        self.pen1 = pg.mkPen(color=(255, 0, 0))
        self.pen2 = pg.mkPen(color=(0, 255, 0))
 
       
    def compare (self):
        self.compareWindow.show()
        com_timedata =  self.timedata
        com_freqdata =   self.alldataabs
          
        if (self.compareflag == 1) :
           
            self.Hide()
            self.compareSound_Plot(com_timedata,com_freqdata,self.compareflag)
           
        elif(self.compareflag == 2):
            self.Show()
            self.mediaplayers[1].setMedia(QMediaContent(QtCore.QUrl.fromLocalFile("F:/eq/cxx.wav")))
            self.compareSound_Plot(com_timedata,com_freqdata,self.compareflag)
        else:
            pass 
    def compareSound_Plot(self,com_timedata,com_freqdata,i):
        self.plot_Time(self.time,com_timedata,self.graphsTime[i+1])
        self.plotFFT(self.freqs,com_freqdata,self.graphsFreq[i+1])
        self.Sound_comp(self.fileName[i],com_timedata,self.mediaplayers[i])
            
    def Hide(self):
        for i in range(len(self.compare2)):
            self.compare2[i].hide()
    def Show(self):
        for i in range(len(self.compare2)):
            self.compare2[i].show()  
    

    def update_duration (self,dur):
        self.progressbars[0].setRange(0,dur)
        print(self.progressbars[0])
    def update_position (self,pos):
        self.progressbars[0].setValue(pos)
    def update_duration1 (self,dur):
        self.progressbars[1].setRange(0,dur)
        print(self.progressbars[1])
    def update_position1 (self,pos):
        self.progressbars[1].setValue(pos)
    def update_duration2 (self,dur):
        self.progressbars[2].setRange(0,dur)
        print(self.progressbars[2])
    def update_position2 (self,pos):
        self.progressbars[2].setValue(pos)        
    
    def Sound_comp (self,filepath,timedata,mediaplayer):
        data1 =np.array(timedata,dtype=np.int16) 
        wavfile.write(filepath,self.samplerate,data1)   
        sound = QMediaContent(QtCore.QUrl.fromLocalFile(filepath))
        mediaplayer.setMedia(sound)

    def change(self):
        if str(self.ui.results.currentText())=="Diff":
            self.diffwindow()
        elif str(self.ui.results.currentText())=="compare":
            self.compareflag +=1 
            if (self.compareflag >= 3):
                pass
            else:
                self.compare()

    def diffwindow(self):  
        self.diffWindow.show()  
        self.differance()       
    def save_file(self):
        self.player.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile("F:/eq/cxx.wav")))
        print(self.timedata)
        data1 =np.array(self.timedata,dtype=np.int16) 
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Open", "", "All Files (.)")
        with open(fileName, 'w') as file:
            wavfile.write(fileName,self.samplerate,data1)    

    def update (self):
        self.player.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile("F:/eq/cxx.wav")))
        data1 =np.array(self.timedata,dtype=np.int16) 
        wavfile.write(self.fileName[0],self.samplerate,data1)   
        sound = QMediaContent(QtCore.QUrl.fromLocalFile(self.fileName[0]))
        self.player.setMedia(sound)

    def getfiles(self):
        path,extention = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",
            "(*.wav )")
        sound = QMediaContent(QtCore.QUrl.fromLocalFile(path))
        if path != '':
            self.player.setMedia(sound) 
        if(path!=''):
            self.read_file(path) 
        else:
            pass       
    def read_file(self,path):
        self.samplerate, self.dataa = wavfile.read(path)
        if (self.dataa.shape[1]==2):
            
            self.dataa = np.mean(self.dataa, axis=1)
        
        self.sample_length = self.dataa.shape[0] 
        self.time = np.arange(self.sample_length) / self.samplerate
        self.plot_Time(self.time,self.dataa,self.graphsTime[0])
        self.FFS(self.dataa,self.samplerate) 
    def FFS(self,data,samplerate):
        self.datafft = fft(data) 
        self.absfftdata = abs(self.datafft)
        self.sample_length =data.shape[0]
        self.freqs = np.fft.fftfreq(self.sample_length,1/samplerate)
        self.plotFFT(self.freqs,self.absfftdata,self.graphsFreq[0])

    def fftintoTime(self,data):
        data_in_timeDomain = np.fft.ifft(data)
        data_in_timeDomain = np.real(data_in_timeDomain)        
        return (data_in_timeDomain)
    def plot_Time(self,time,data,graphT):  
        graphT.showGrid(True)
        graphT.plot(time,data,pen=self.pen1)

    def plotFFT(self,freqs,data,graphF):  
        graphF.setXRange(-self.samplerate/2, self.samplerate/2)
        graphF.showGrid(True)
        graphF.setYRange(0, max(data))
        graphF.plot(freqs[:int(freqs.size)],data[:int(freqs.size)],pen=self.pen2)
        self.Bands(data.size)
    
    
    def Bands(self,size): 

        bandsno = math.ceil(0.05 * size)
        self.bands =[self.datafft[i * bandsno:(i + 1) * bandsno] for i in range(0,20)]        
     
    def hamming(self,i,length1,length2):
        value = self.sliders[i].value()
        self.texts[i].setText(str(value))
        if value<0:
            value= 1/abs(value)
        hamm1 = np.hamming(length1)
        band1 = self.bands[i] * hamm1 *value
        hamm2 = np.hamming(length2)
        band2 = self.bands[self.numBands-1-i] * hamm2 *value
        return band1,band2
  
    def hanning(self,i,length1,length2):
        value = self.sliders[i].value()
        self.texts[i].setText(str(value))
        if value<0:
            value= 1/abs(value)
        hamm1 = np.hanning(length1)
        band1 = self.bands[i] * hamm1 *value
        hamm2 = np.hanning(length2)
        band2 = self.bands[self.numBands-1-i] * hamm2 *value
        return band1,band2
   
    def rect(self,i):
        value = self.sliders[i].value()
        self.texts[i].setText(str(value))
        if value<0:
            value= 1/abs(value)
        band1 = self.bands[i] *value
        band2 = self.bands[self.numBands-1-i] *value
        return band1,band2
   
    def Gain (self):
        if (self.datafft.size>0):
            self.ui.DataAfterEdit_Time.clear()
            self.ui.DataAfterEdit_Freq.clear()
            band= []
            band = self.bands[:]
            for i in range(self.numSliders):
                length1=len(band[i])
                length2=len(band[self.numBands-1-i])
                if (str(self.ui.options.currentText())=="Hamm"):

                    band[i],band[self.numBands-1-i]= self.hamming(i,length1,length2)

                elif (str(self.ui.options.currentText())=="Hann"):
                    
                    band[i],band[self.numBands-1-i]= self.hanning(i,length1,length2)

                elif(str(self.ui.options.currentText())=="Rect"):
                    band[i],band[self.numBands-1-i]= self.rect(i)
            
                else:
                    band[i] = self.bands[i]
                    band[self.numBands-1-i] = self.bands[self.numBands-1-i] 

            # self.bands[0][:int(self. bands[0].size *.25)]=0
            band[1]=band[1]*0
            band[18]=band[18]*0
            band[11] =band[11]* 0
            alldata = np.concatenate(band)
            self.alldataabs = np.abs(alldata)
            self.timedata = self.fftintoTime(alldata)
            self.plot_Time(self.time,self.timedata,self.graphsTime[1])
            self.plotFFT(self.freqs,self.alldataabs,self.graphsFreq[1])
            self.diffTimeData = self.timedata-self.dataa
            self.diffFreqData =np.abs(self.alldataabs- self.absfftdata)
            self.update()
            

    def differance(self):
        self.plot_Time(self.time,self.diffTimeData,self.graphsTime[4])
        self.plotFFT(self.freqs,self.diffFreqData,self.graphsFreq[4])
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()