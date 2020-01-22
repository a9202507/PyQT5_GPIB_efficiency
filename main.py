import sys
import gpib
import Chroma
from PyQt5.QtWidgets import QMainWindow,QApplication,QTableView
import Ui_PyQt_Chroma_Eload_GUI
import PdQtClass
import measure
import time
import datetime
import os
import pandas as pd

class MyMainWindow(QMainWindow,Ui_PyQt_Chroma_Eload_GUI.Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.commandLinkButton.clicked.connect(self.pushButton_Click)
        self.pushButton.clicked.connect(self.detectGPIB)
        self.pushButton_2.clicked.connect(self.openDf_csv)
        self.pushButton_3.clicked.connect(self.pushbutton3)
        
        ##to do , select checkbox then goto next step
        ##self.checkBox_1.checked.connect(self.setNextOn)
        
       
        
        #set DC source On
        self.pushButton_4.clicked.connect(self.dcsourceOn)
        #set DC source Off
        self.pushButton_5.clicked.connect(self.dcsourceOff)
       
        self.show()
        self.time=str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.filename=self.time+".csv"
        #set defalut file name
        self.lineEdit.setText(self.filename)
        self.df=pd.DataFrame()

        #set "open reuslt" button isn't work in GUI init.
        self.pushButton_2.setEnabled(False)

        #set comboBox value
        self.comboBox.setCurrentText("7")
        #self.comboBox.setEnabled(True)
        self.comboBox_2.setCurrentText("9")
        #self.comboBox_2.setEnabled(True)
        self.comboBox_3.setCurrentText("5")
        
        
    def openDf_csv(self):
        self.filename=self.lineEdit.text()
        self.df.to_csv(self.filename)
        os.system("start excel.exe %s" % self.filename)
       
    def pushButton_Click(self):
        loadlist=list()
        Iout_max=int(self.lineEdit_2.text())
        Iout_step=int(self.lineEdit_3.text())
        Delay=int(self.lineEdit_4.text())
        gpibaddr1=int(self.comboBox.currentText())
        gpibaddr2=int(self.comboBox_2.currentText())
        if self.checkBox_1.isChecked():
            load1=gpib.ChromaEload(gpibaddr1,1,int(self.lineEdit_L1.text()),0)
            loadlist.append(load1)
            
            
        if self.checkBox_3.isChecked():
            load3=gpib.ChromaEload(gpibaddr1,3,30,0)
            loadlist.append(load3)

        if self.checkBox_5.isChecked():
            load5=gpib.ChromaEload(gpibaddr1,5,30,0)
            loadlist.append(load5)
            
        if self.checkBox_7.isChecked():
            load7=gpib.ChromaEload(gpibaddr1,7,30,0)
            loadlist.append(load7)

        if self.checkBox_9.isChecked():
            load9=gpib.ChromaEload(gpibaddr1,9,30,0)
            loadlist.append(load9)
            
        if self.checkBox_51.isChecked():
            load51=gpib.ChromaEload(gpibaddr2,1,30,0)
            loadlist.append(load51)
            
        
         
        #df=measure.measureEfficiency(loadlist,Iout_max,Iout_step,Delay)
        if self.checkBox.isChecked():
            df=measure.measureEfficiency(loadlist,Iout_max,Iout_step,Delay, 1)
        else:
            df=measure.measureEfficiency(loadlist,Iout_max,Iout_step,Delay, 0)
            
            
        #self.textBrowser.setText("Efficiency finish")

        self.showdf(df)
        self.df=df
        self.pushButton_2.setEnabled(True)
        self.reflash_filename()
        
        
    def detectGPIB(self):
        df=gpib.scanGPIB()
        self.showdf(df)
    
    def showdf(self,df):
        model=PdQtClass.pandasModel(df)
        view = QTableView()
        view.setModel(model)
        view.resize(800,600)
        self.w=QTableView()
        self.w.setModel(model)
        self.w.resize(480,320)
        self.w.show()
    
    # for test button
    def pushbutton3(self):
        
        self.pushButton_2.setEnabled(True)
        self.filename=self.lineEdit.text()
        print(self.time)
        print(self.filename)
        self.reflash_filename()
        self.pushButton_4.setStyleSheet('background-color: Red') 

    def reflash_filename(self):
        self.time=str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.filename=self.time+".csv"
        self.lineEdit.setText(self.filename)
    
    #set DC source 
    def dcsourceOn(self):
        voltage=float(self.lineEdit_5.text())
        current=int(self.lineEdit_6.text())
        gpibaddr=int(self.comboBox_3.currentText())
        print(f'{voltage}, {current}, {gpibaddr}')
        dcsource=gpib.AgilentDCsource(gpibaddr, voltage, current)
        dcsource.On()
        self.pushButton_4.setStyleSheet('background-color: Red') 
        None
    def dcsourceOff(self):
        voltage=float(self.lineEdit_5.text())
        current=int(self.lineEdit_6.text())
        gpibaddr=int(self.comboBox_3.currentText())
        dcsource=gpib.AgilentDCsource(gpibaddr, voltage, current)
        dcsource.Off()
        self.pushButton_4.setStyleSheet('background-color: None')
    
    ## to do , select checkbox then goto next step
    def setNextOn(self):
         None
    


if __name__ == "__main__":
    app=QApplication(sys.argv)

    myWin=MyMainWindow()

    myWin.show()

    sys.exit(app.exec_())
