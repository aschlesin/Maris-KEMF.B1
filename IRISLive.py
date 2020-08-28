# -*- coding: utf-8 -*-

"""
Basic GUI application to get near real-time readings from IRIS to determine
the change in dip for an instrument. Streams are at a 1 second delay 
(excluding any buffer times based on internet). Once 3 URLs are entered into
the form from IRIS, click "start" and the application will calculate the dip
of the 3 channels.

When finished, press "stop" and a log file titled "DipLog.txt" will be
generated in the parent folder.

NOTE TO USERS: Threading is not perfect! To exit from the application, DO NOT
CLICK THE 'X' button! Please hit 'Stop' before exiting. There will be lag in
in the application.
"""

from PyQt5 import QtGui, QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
from obspy.clients.fdsn import Client
from obspy import Stream, read
import datetime
client = Client("IRIS")

import matplotlib.pyplot as plt

class Ui_Form(object):
    
    def setupUi(self, Form):
        
        self.startstop = 0
        
        
        #   Define main application
        Form.setObjectName("Form")
        Form.resize(1500, 800)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        
        
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        
        #   URL Grabs (Z) text field
        self.URLGrabZ = QtWidgets.QLineEdit(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.URLGrabZ.setFont(font)
        self.URLGrabZ.setText("Paste Z-Axis URL Here")
        self.URLGrabZ.setObjectName("URLGrabZ")
        self.gridLayout_3.addWidget(self.URLGrabZ, 1, 0, 1, 1)
        
        #  URL Grabs (N) text field 
        self.URLGrabN = QtWidgets.QLineEdit(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.URLGrabN.setFont(font)
        self.URLGrabN.setText("Paste N-Axis URL Here")
        self.URLGrabN.setObjectName("URLGrabN")
        self.gridLayout_3.addWidget(self.URLGrabN, 2, 0, 1, 1)
        
        #  URL Grabs (E) text field 
        self.URLGrabE = QtWidgets.QLineEdit(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.URLGrabE.setFont(font)
        self.URLGrabE.setText("Paste E-Axis URL Here")
        self.URLGrabE.setObjectName("URLGrabE")
        self.gridLayout_3.addWidget(self.URLGrabE, 3, 0, 1, 1)
        
        # Start button
        self.StartB = QtWidgets.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.StartB.setFont(font)
        self.StartB.setObjectName("StartB")
        self.gridLayout_3.addWidget(self.StartB, 4, 0, 1, 1)
        self.StartB.clicked.connect(self.started)
        
        #   Stop button
        self.StopB = QtWidgets.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.StopB.setFont(font)
        self.StopB.setObjectName("StopB")
        self.gridLayout_3.addWidget(self.StopB, 5, 0, 1, 1)
        self.StopB.clicked.connect(self.stopped)
        
        #   Random labels/frames
        self.gridLayout.addWidget(self.groupBox_3, 1, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        self.xtilt = QtWidgets.QLabel(self.groupBox_4)
        self.xtilt.setObjectName("xtilt")
        self.gridLayout_4.addWidget(self.xtilt, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)
        self.ytilt = QtWidgets.QLabel(self.groupBox_4)
        self.ytilt.setObjectName("ytilt")
        self.gridLayout_4.addWidget(self.ytilt, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 2, 0, 1, 1)
        self.ztilt = QtWidgets.QLabel(self.groupBox_4)
        self.ztilt.setObjectName("ztilt")
        self.gridLayout_4.addWidget(self.ztilt, 2, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        
        self.degS = u"\u00b0" #  Degree sign

        #   Live Wave
        self.LiveWaveFigure = Figure()
        self.LiveWave = FigureCanvas(self.LiveWaveFigure)
        self.gridLayout_2.addWidget(self.LiveWave, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)
        
        #   Generate Live Tilt plot
        fig1, (self.ax1, self.ax2, self.ax3) = plt.subplots(1,3,subplot_kw=dict(polar=True))
        #   Z-channel tiltmeter
        self.ax1.plot(0,1)
        self.ax1.set_theta_direction(-1)
        self.ax1.set_theta_zero_location("E")
        self.ax1.set_thetamin(-90)
        self.ax1.set_thetamax(90)
        self.ax1.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
        self.ax1.set_yticklabels([])
        self.ax1.set_title("Z-Channel Dip", pad = 20, size = 18)
        self.ax1.set_xticklabels(['-90'+self.degS + '\n(Up)','-75'+self.degS,'-60'+self.degS,'-45'+self.degS,'-30'+self.degS,'-15'+self.degS,'0'+self.degS + "\n(Seafloor)",'15'+self.degS,'30'+self.degS,'45'+self.degS,'60'+self.degS,'75'+self.degS,'90'+self.degS +'\n(Down)'], size = 10)
        
        #   N-channel tiltmeter
        self.ax2.plot(0,1)
        self.ax2.set_theta_direction(-1)
        self.ax2.set_theta_zero_location("E")
        self.ax2.set_thetamin(-90)
        self.ax2.set_thetamax(90)
        self.ax2.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
        self.ax2.set_yticklabels([])
        self.ax2.set_title("N-Channel Dip", pad = 20, size = 18)
        self.ax2.set_xticklabels(['-90'+self.degS + '\n(Up)','-75'+self.degS,'-60'+self.degS,'-45'+self.degS,'-30'+self.degS,'-15'+self.degS,'0'+self.degS + "\n(Seafloor)",'15'+self.degS,'30'+self.degS,'45'+self.degS,'60'+self.degS,'75'+self.degS,'90'+self.degS +'\n(Down)'], size = 10)
        
        #   E-channel tiltmeter
        self.ax3.plot(0,1)
        self.ax3.set_theta_direction(-1)
        self.ax3.set_theta_zero_location("E")
        self.ax3.set_thetamin(-90)
        self.ax3.set_thetamax(90)
        self.ax3.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
        self.ax3.set_yticklabels([])
        self.ax3.set_title("E-Channel Dip", pad = 20, size = 18)
        self.ax3.set_xticklabels(['-90'+self.degS + '\n(Up)','-75'+self.degS,'-60'+self.degS,'-45'+self.degS,'-30'+self.degS,'-15'+self.degS,'0'+self.degS + "\n(Seafloor)",'15'+self.degS,'30'+self.degS,'45'+self.degS,'60'+self.degS,'75'+self.degS,'90'+self.degS +'\n(Down)'], size = 10)
        
        
        #   Live Tilt
        self.LiveTilt = FigureCanvas(fig1)
        self.gridLayout_2.addWidget(self.LiveTilt, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        
    def started(self):
        
        #   Log file header
        logger = "Time(UTC)\t\tZ-Channel Dip\tN-Channel Dip\tE-Channel Dip"
        
        #   Retrieve the 3 URLs
        fullURL = [str(self.URLGrabZ.text()),
                   str(self.URLGrabN.text()),
                   str(self.URLGrabE.text())]
        
        #   Parse the front and back ends of the URL to single out the changing time
        #   Will create a list of lists going z channel, n channel, and e channel
        #   each sublist will be the front of the URL then the end of the URL
        URLParse = [[fullURL[0][:fullURL[0].find('start=')],fullURL[0][(fullURL[0].rfind('&end=') + 24):]],
                    [fullURL[1][:fullURL[1].find('start=')],fullURL[1][(fullURL[1].rfind('&end=') + 24):]],
                    [fullURL[2][:fullURL[2].find('start=')],fullURL[2][(fullURL[2].rfind('&end=') + 24):]]]
        
        #   Get the channel names
        chans = [(fullURL[0][fullURL[0].find('cha=')+4:])[0:3], #z channel
                 (fullURL[1][fullURL[1].find('cha=')+4:])[0:3], #n channel
                 (fullURL[2][fullURL[2].find('cha=')+4:])[0:3]] #e channel
        
        #   Get the current time of the button press
        gettimeNow = datetime.datetime.now()-datetime.timedelta(seconds=1)

        
        #   Generate the time strings for the URL
        #   Time is 1 second behind real time to allow for buffering
        t_start = str((gettimeNow-datetime.timedelta(seconds=1)).date())+'T'+str((gettimeNow-datetime.timedelta(seconds=1)).time())
        t = str(gettimeNow.date())+'T'+str(gettimeNow.time())
        
        #   Stop button setter
        self.startstop = 1
        
        while self.startstop ==1:
            #   Combine the string for the URL
            timestring = 'start=' + t_start + '&end=' + t
            
            #   Make the stream variable
            st = Stream()
                  
            #   Get data
            for i in range(3):        
                url = URLParse[i][0] + timestring + URLParse[i][1]
                st.append(read(url)[0])
                print(chans[i])
        
            
            #   Get the mean for gravity from the channels
            Zchan = np.mean(st.select(channel=chans[0])[0].data)
            Nchan =  np.mean(st.select(channel=chans[1])[0].data)
            Echan =  np.mean(st.select(channel=chans[2])[0].data)
            QtWidgets.QApplication.processEvents()
            
            g = np.sqrt(Zchan**2+Nchan**2+Echan**2)

            
            # Get the current angles for each channel
            alpha_N = np.arcsin(Nchan/g)*180/np.pi
            alpha_E = np.arcsin(Echan/g)*180/np.pi
            alpha_Z = np.arccos(Zchan/g)*180/np.pi
            print(t + " Z: " + str(alpha_Z) + " N: " + str(alpha_N) + " E: " + str(alpha_E))
            QtWidgets.QApplication.processEvents()
            
            #   Generate the tilt plot
            #   Define the figure
            self.ax1.clear()
            self.ax2.clear()
            self.ax3.clear()

            #   Z-channel tiltmeter
            self.ax1.plot(0,1)
            self.ax1.arrow(float(alpha_Z)/180*np.pi,0,0,0.82,
                                  width = 0.05, edgecolor = 'black', facecolor = 'blue', lw = 2, zorder = 2)
            self.ax1.set_theta_direction(-1)
            self.ax1.set_theta_zero_location("E")
            self.ax1.set_thetamin(-90)
            self.ax1.set_thetamax(90)
            self.ax1.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
            self.ax1.set_yticklabels([])
            self.ax1.set_title("Z-Channel Dip", pad = 20, size = 18)
            self.ax1.set_xticklabels(['-90'+self.degS + '\n(Up)','-75'+self.degS,'-60'+self.degS,'-45'+self.degS,'-30'+self.degS,'-15'+self.degS,'0'+self.degS + "\n(Seafloor)",'15'+self.degS,'30'+self.degS,'45'+self.degS,'60'+self.degS,'75'+self.degS,'90'+self.degS +'\n(Down)'], size = 10)
            
            #   N-channel tiltmeter
            self.ax2.plot(0,1)
            self.ax2.arrow(float(alpha_N)/180*np.pi,0,0,0.82,
                                  width = 0.05, edgecolor = 'black', facecolor = 'blue', lw = 2, zorder = 2)
            self.ax2.set_theta_direction(-1)
            self.ax2.set_theta_zero_location("E")
            self.ax2.set_thetamin(-90)
            self.ax2.set_thetamax(90)
            self.ax2.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
            self.ax2.set_yticklabels([])
            self.ax2.set_title("N-Channel Dip", pad = 20, size = 18)
            self.ax2.set_xticklabels(['-90'+self.degS + '\n(Up)','-75'+self.degS,'-60'+self.degS,'-45'+self.degS,'-30'+self.degS,'-15'+self.degS,'0'+self.degS + "\n(Seafloor)",'15'+self.degS,'30'+self.degS,'45'+self.degS,'60'+self.degS,'75'+self.degS,'90'+self.degS +'\n(Down)'], size = 10)
            
            #   E-channel tiltmeter
            self.ax3.plot(0,1)
            self.ax3.arrow(float(alpha_E)/180*np.pi,0,0,0.82,
                                 width = 0.05, edgecolor = 'black', facecolor = 'blue', lw = 2, zorder = 2)
            self.ax3.set_theta_direction(-1)
            self.ax3.set_theta_zero_location("E")
            self.ax3.set_thetamin(-90)
            self.ax3.set_thetamax(90)
            self.ax3.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
            self.ax3.set_yticklabels([])
            self.ax3.set_title("E-Channel Dip", pad = 20, size = 18)
            self.ax3.set_xticklabels(['-90'+self.degS + '\n(Up)','-75'+self.degS,'-60'+self.degS,'-45'+self.degS,'-30'+self.degS,'-15'+self.degS,'0'+self.degS + "\n(Seafloor)",'15'+self.degS,'30'+self.degS,'45'+self.degS,'60'+self.degS,'75'+self.degS,'90'+self.degS +'\n(Down)'], size = 10)
            
            #   Draw the updates to the angle
            self.ax1.figure.canvas.draw()
            self.ax2.figure.canvas.draw()
            self.ax3.figure.canvas.draw()
            
            #   Show the analog tilt update
            self.xtilt.setText(str(round(alpha_Z,2)))
            self.ytilt.setText(str(round(alpha_N,2)))
            self.ztilt.setText(str(round(alpha_E,2)))
            QtWidgets.QApplication.processEvents()
            
            
            #   Draw the obspy figure
            self.LiveWaveFigure.clf()
            st.plot(fig = self.LiveWaveFigure, draw = True)
            gettimeNow = datetime.datetime.now()-datetime.timedelta(seconds=1)

            t_start = t
            t = str(gettimeNow.date())+'T'+str(gettimeNow.time())
            logger += "\n" + t + '\t' + str(round(alpha_Z,5)) + '\t' + str(round(alpha_N,5)) + '\t' + str(round(alpha_E,5))
            QtWidgets.QApplication.processEvents()
            

      
        #   When the stream is cancelled, print a log of the dips
        if self.startstop == 0:
            with open('DipLog.txt','w') as t:
                t.write(logger)
            Form.close() #  Close the application

    #   Button to press that stops the stream and gets the dip log
    def stopped(self):
        self.startstop = 0
        print(self.startstop)

    #   Define base labels/titles
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_3.setTitle(_translate("Form", "Station Selector"))
        self.label.setText(_translate("Form", "Generate a URL from IRIS Timeseries builder and copy into the text field below.\n(URL Builder: http://service.iris.edu/irisws/timeseries/docs/1/builder/)"))
        self.StartB.setText(_translate("Form", "Start"))
        self.StopB.setText(_translate("Form", "Stop"))
        self.groupBox_2.setTitle(_translate("Form", "Live Tilt Calculation"))
        self.groupBox_4.setTitle(_translate("Form", "Channel Orientation"))
        self.label_2.setText(_translate("Form", "Z-Channel:"))
        self.label_4.setText(_translate("Form", "N-Channel:"))
        self.label_3.setText(_translate("Form", "E-Channel:"))
        self.groupBox.setTitle(_translate("Form", "Live Waveform Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

