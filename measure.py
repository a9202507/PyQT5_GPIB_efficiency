import gpib
import pandas as pd
import time
import matplotlib.pyplot as plt


def daqMeasure(df):
    daq=gpib.AgilentDAQ(10,110,111,103,101)
    daq.ReadVin()
    daq.ReadIin()
    daq.ReadVout()
    daq.ReadRemoteVout()
    pdtemp={}
    pdtemp['Vin']=daq.vinValue
    pdtemp['Iin']=daq.iinValue
    pdtemp['Vout']=daq.voutValue
    pdtemp['VoutRemote']=daq.voutRemoteValue
    df=df.append(pdtemp,ignore_index=True)
    return df

def EloadOnoff(Eloadlist,Iout,OnOff):
    if OnOff == 1:
        for __ in range(0,len(Eloadlist)):
            Eloadlist[__].setCurrent(Iout/len(Eloadlist))
            Eloadlist[__].on()
    else:
        for __ in range(0,len(Eloadlist)):
            Eloadlist[__].off()
              

def measureEfficiency(loadlist,Ioutmax,Ioutstep,delaytime,onlivecurve=1):
    

    EloadOnoff(loadlist,0,1)
    df=pd.DataFrame()
    i=0
    ax=[]
    ay=[]
    ay1=[]
    for current in range(0,Ioutmax+1,Ioutstep):
        Iout=0
        
        
        EloadOnoff(loadlist,current,1)
        df=daqMeasure(df)
        time.sleep(delaytime)
        for __ in range(0,len(loadlist)):
            loadlist[__].measureCurrent()
            Iout+=loadlist[__].meascurrent
        df.loc[i,"Iout"]=Iout
        df.loc[i,"Effi"]=(df.loc[i,"Vout"]*df.loc[i,"Iout"])/(df.loc[i,"Vin"]*df.loc[i,"Iin"])
        df.loc[i,"EffiRemote"]=(df.loc[i,"VoutRemote"]*df.loc[i,"Iout"])/(df.loc[i,"Vin"]*df.loc[i,"Iin"])
        
        #plt cruve
        if onlivecurve==1:
            ax.append(df.loc[i,'Iout'])
            ay.append(df.loc[i,'Effi'])
            ay1.append(df.loc[i,'EffiRemote'])        
            i+=1
            plt.clf()
            plt.ion()
            plt.plot(ax,ay)
            plt.plot(ax,ay1)
            plt.pause(0.1)
            plt.ioff()
        else:
            None

##    use df.plt to show cruve.
##    df.plot(x='Iout',y='Vout')
##    plt.show()


        
    EloadOnoff(loadlist,0,0)
    return df
        
    

if __name__ =="__main__":
    load5=gpib.ChromaEload(7,5,30,0)
    load9=gpib.ChromaEload(7,9,50,0)
    load63=gpib.ChromaEload(9,1,100,0)
    loadlist=[load5,load9,load63]
    df=measureEfficiency(loadlist,100,10,1,1)
    results=pd.DataFrame(df,columns=['Vin','Iin','Vout','VoutRemote','Iout'])
    #results.to_csv("20200114.csv")
    print(df)
