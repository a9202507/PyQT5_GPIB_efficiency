# ChromaEload Class 

import visa                                                     # import GPIB module
import time
import pandas as pd
import datetime
import os

class ChromaEload:
    def __init__(self,GPIBaddr,EloadChannel,currentCapability=0,loading=0):
        # init PyVISA for GPIB control 
        self.gpibaddr=GPIBaddr
        self.rm=visa.ResourceManager()
        self.device=visa.ResourceManager().open_resource('GPIB0::'+str(GPIBaddr)+'::INSTR')

        # loading current in Chroma machine
        self.current=loading

        #channel setting of Chroma machine
        self.channel=EloadChannel

        #setting max currnet
        self.currentCapability=currentCapability

      
        #disable all run off
        self.device.write('CONF:ALLR 0')
        
        ## detect vendor,model name then save to self.vendor and self.model 
        IDN=self.device.query('*IDN?')
        self.vendor=IDN[:(IDN.find(","))]
        char_s=IDN.find(",")    # find 1st ","
        char_e=IDN.find(",",(char_s)+1) #find 2nd ","
        self.model=IDN[char_s+1:char_e]

        self.setCurrent(self.current)

    #turn on single channel
    def on(self):
        self.device.write('CHAN '+str(self.channel))
        self.device.write('CURR:STAT:L1 '+str(self.current))
        self.device.write('LOAD ON')
        #self.device.write('CHAN '+str(self.channel)+':ACT ON')

    #turn off single channel
    def off(self):
        #self.device.write('CHAN '+str(self.channel)+':ACT OFF')
        self.device.write('CHAN '+str(self.channel))
        self.device.write('LOAD OFF')

    #turn on all channel
    def allOn(self):
        self.device.write('RUN')

    #turn off all channel
    def allOff(self):
        self.device.write('Abort')
        
    def setCurrent(self,current):
        self.current=current
        self.device.write('CHAN '+str(self.channel))
        self.device.write('CURR:STAT:L1 '+str(self.current))
        
    def setGpibAddr(self,gpibaddr):
        self.gpibaddr=gpibaddr
        
    def measureCurrent(self):
        self.device.write("CHAN "+str(self.channel))
        self.meascurrent=self.device.query_ascii_values('FETC:CURR?')[0]
        

class AgilentDCsource:
    def __init__(self,GPIBaddr,maxVoltage=0,maxCurrent=0):
        self.gpibaddr=GPIBaddr
        self.rm=visa.ResourceManager()
        self.device=visa.ResourceManager().open_resource('GPIB0::'+str(GPIBaddr)+'::INSTR')
        self.voltage=maxVoltage
        self.current=maxCurrent
        IDN=self.device.query('*IDN?')
        self.vendor=IDN[:(IDN.find(","))]
        char_s=IDN.find(",")    # find 1st ","
        char_e=IDN.find(",",(char_s)+1) #find 2nd ","
        self.model=IDN[char_s+1:char_e]
         
        self.setVoltage(self.voltage)
        self.setCurrent(self.current)

    def On(self):
        self.device.write('OUTPUT:STATE ON')

    def Off(self):
        self.device.write('OUTPUT:STATE OFF')

    def setCurrent(self,current):
        self.current=current
        self.device.write('SOURce:CURRent '+str(self.current))
    def setVoltage(self,voltage):
        self.voltage=voltage
        self.device.write('SOURce:VOLTage '+str(self.voltage))
    def setGpibAddr(self,gpibaddr):
        self.gpibaddr=gpibaddr

class AgilentDAQ:
    def __init__(self,GPIBaddr,VinChannel=0,IinChannel=0,VoutChannel=0,VoutRemoteChannel=0):
        self.gpibaddr=GPIBaddr
        self.rm=visa.ResourceManager()
        self.device=visa.ResourceManager().open_resource('GPIB0::'+str(GPIBaddr)+'::INSTR')
        IDN=self.device.query('*IDN?')
        self.vendor=IDN[:(IDN.find(","))]
        char_s=IDN.find(",")    # find 1st ","
        char_e=IDN.find(",",(char_s)+1) #find 2nd ","
        self.model=IDN[char_s+1:char_e]
        self.vinChannel=str(VinChannel)
        self.vinValue=0
        self.iinChannel=str(IinChannel)
        self.iinValue=0
        self.voutChannel=str(VoutChannel)
        self.voutValue=0
        self.voutRemoteChannel=str(VoutRemoteChannel)
        self.voutRemoteValue=0

    def ReadVin(self):
        self.device.write('MEAS:VOLT:DC? Auto,DEF,(@'+str(self.vinChannel)+")")          # measure Vin value for DAQ machine.
        self.vinValue=(float(self.device.read()))

    def ReadIin(self):
        self.device.write('MEAS:VOLT:DC? Auto,DEF,(@'+str(self.iinChannel)+")")          # measure Vin value for DAQ machine.
        self.iinValue=((float(self.device.read()))/0.00025) #0.00025 mean R-shunt is 0.25mhoms.

    def ReadVout(self):
        self.device.write('MEAS:VOLT:DC? Auto,DEF,(@'+str(self.voutChannel)+")")          # measure Vin value for DAQ machine.
        self.voutValue=(float(self.device.read()))
    def ReadRemoteVout(self):
        self.device.write('MEAS:VOLT:DC? Auto,DEF,(@'+str(self.voutRemoteChannel)+")")          # measure Vin value for DAQ machine.
        self.voutRemoteValue=(float(self.device.read()))

def measureEffi(loadlist,results,delaytime):

    results=results
    time.sleep(delaytime)
    for dev in range(0,len(loadlist)):
        loadlist[dev].measureCurrent()

    
    daq.ReadVin()
    daq.ReadIin()
    daq.ReadVout()
    daq.ReadRemoteVout()
    pdtemp={}
    pdtemp['Vin']=daq.vinValue
    pdtemp['Iin']=daq.iinValue
    pdtemp['Vout']=daq.voutValue
    pdtemp['VoutRemote']=daq.voutRemoteValue
##    pdtemp['CH1']=load1.meascurrent
##    pdtemp['CH3']=load3.meascurrent
##    pdtemp['CH5']=load5.meascurrent
##    pdtemp['CH7']=load7.meascurrent
##    pdtemp['CH9']=load9.meascurrent
##    pdtemp['CH63']=load63.meascurrent
    Iout=0
    for dev in range(0,len(loadlist)):
        Iout+=loadlist[dev].meascurrent
    
    #Iout=load1.meascurrent+load3.meascurrent+load5.meascurrent+load7.meascurrent+load9.meascurrent+load63.meascurrent
    pdtemp['Iout']=Iout
    efficiency=((daq.voutValue*Iout)/(daq.vinValue*daq.iinValue))*100
    efficiency_remote=((daq.voutRemoteValue*Iout)/(daq.vinValue*daq.iinValue))*100
    pdtemp['Effi']=efficiency
    pdtemp['Effi_Remote']=efficiency_remote
    results=results.append(pdtemp,ignore_index=True)
    #print(f"{daq.vinValue}\t\t{daq.iinValue}\t\t{daq.voutValue}\t\t{Iout}A\t\t{efficiency}")
    return results

def main(loadlist,daq,Imax,Istep,results,delaytime):
    while Imax>0:
        for dev in range(0,len(loadlist)):
            loadlist[dev].on()
            #print(f"{dev}, device")
            

                 
            while loadlist[dev].currentCapability>loadlist[dev].current:
                loadlist[dev].setCurrent(loadlist[dev].current+Istep)
                loadlist[dev].on()
                #print(f"{loadlist[dev].channel} current = ,{loadlist[dev].current}")
                Imax-=Istep
                results=measureEffi(loadlist,results,delaytime)
                if Imax <0:
                    break
    #print("finish")

    for dev in range(0,len(loadlist)):
        loadlist[dev].off()


    results=pd.DataFrame(results,columns=['Vin','Iin','Vout','VoutRemote','Iout','Effi','Effi_Remote',"CH1","CH3","CH5","CH7","CH9","CH63"])
    #results=pd.DataFrame(results,columns=['Vin','Iin','Vout','VoutRemote','Iout','Effi','Effi_Remote'])
    theTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")    
    file_name=str(theTime)+".csv"
    results.to_csv(file_name)
    os.system("start excel.exe %s" % file_name)
        
    
        
if __name__ =="__main__":

    daq=AgilentDAQ(10,110,111,103,101)
    #set each loading max loading current capability 
    load1=ChromaEload(7,1,80,0)
    load3=ChromaEload(7,3,50,0)
    load5=ChromaEload(7,5,80,0)
    load7=ChromaEload(7,7,80,0)
    load9=ChromaEload(7,9,80,0)
    # this is another Chroma loading and GPIB=9
    load63=ChromaEload(9,1,100,0)
    
    #Create list to store all ChromeEload Obj.
    loadlist=[load1,load7,load63]
    results=pd.DataFrame()
    main(loadlist,daq,201,20,results,1)


    

