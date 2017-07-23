import re
import os
from datetime import datetime, date
import time
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
from operator import itemgetter
import cPickle as pickle

def removeOutliers(datalist) : 
    for x in datalist :
        if x < 0. :
            print x, "NEGATIVE TIME!!!!!!!"
            datalist.remove(x)
    data = np.asarray(datalist)
    tmpMean = data.mean()
    tmpStd = data.std()
    print tmpMean, tmpStd
    newlist =[]
    for x in datalist :
        if (x > (tmpMean - 2*tmpStd)) and (x < (tmpMean +2*tmpStd)):
	    newlist.append(x)
    newdata = np.asarray(newlist)
    print newdata
    print newdata.mean(),newdata.std()
    return newdata

def selectChipCondition(dic,char) :
    isReject = False
    if (dic.get('chipOK')) and ((dic.get('Finish') - dic.get('Start')).total_seconds()<0) :
        isReject = True
        return isReject
    if char=="OK" :
        if (not (dic.get('chipOK'))) :
            isReject = True
            return isReject
        if (dic.get('chipOK')) and ((dic.get('Finish') - dic.get('Start')).total_seconds()>1000) :
            isReject = True
            return isReject
    if char=="NK" :
        if (not (dic.get('chipOK'))) and ((dic.get('Finish') - dic.get('Start')).total_seconds()>500) :
            isReject = True
            return isReject
        if (dic.get('chipOK')) :
            isReject = True
            return isReject
    if char=="ALL" :
        if (not (dic.get('chipOK'))) and ((dic.get('Finish') - dic.get('Start')).total_seconds()>500) :
            isReject = True
            return isReject
        if (dic.get('chipOK')) and ((dic.get('Finish') - dic.get('Start')).total_seconds()>1000) :
            isReject = True
            return isReject
    return isReject

def getlistname(inputlist):
    for key, value in globals().iteritems() :
        if type(value) == list and value == inputlist   :
            return key

def plot_process(data,dataname,char) :
    if char=="OK" :
        y, x, _ = plt.hist(data,facecolor='mediumseagreen',align='mid')
        plt.axvline(data.mean(), color='green', linestyle='dashed', linewidth=2)
    if char=="NK" :
        y, x, _ = plt.hist(data,facecolor='tomato',align='mid')
        plt.axvline(data.mean(), color='crimson', linestyle='dashed', linewidth=2)
    if char=="ALL" :
        y, x, _ = plt.hist(data,facecolor='steelblue',align='mid')
        plt.axvline(data.mean(), color='navy', linestyle='dashed', linewidth=2)
    print x.max()
    print y.max()
    plt.title(dataname)
    plt.xlabel("time [s]")
    plt.ylabel("number of entries")
    plt.ylim(0,y.max()+2)
    plt.xlim(x.min()-2.*np.std(data),x.max()+2.*np.std(data))
    mu = data.mean()
    median = np.median(data)
    sigma = data.std()
    entry = data.size
    textstr = '$\mathrm{mean}=%.2f$\n$\mathrm{median}=%.2f$\n$\sigma=%.2f$\n$\mathrm{N}=%i$'%(mu, median, sigma,entry)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(x.max(), y.max()+1, textstr, fontsize=14,verticalalignment='top')
    plt.savefig("./plots/" + dataname + "_" + char + ".pdf")
    plt.close()

def analyze_process(inputlist,char):
    datalist = inputlist
    dataname = getlistname(inputlist)
    data = removeOutliers(datalist)
    print "########################", dataname, "########################"
    print "# of Entries : ",np.prod(data.shape),"\n Mean time : ", np.mean(data),"\n Standard deviation : ", np.std(data)
    plot_process(data,dataname,char)


tray_to_ppc = []
dimension_check = []
edge_integrity = []
probecard_measurement_total = []
ppc_to_tray = []
total_time = []

probecard_measurement_initialization_1st = []
probecard_measurement_initialization_2nd = []
probecard_measurement_1st = []
probecard_measurement_2nd= []
chipCondition="ALL"#arguments can be "OK","NK","ALL"
dirName = './result'
fileList = os.listdir(dirName)
fileChipbyChip = open("chipbychip_result.csv", 'w')
fileChipbyChip.write("Time,TrayID,ChipID,Status,TotalTime,Init,Dim,Edge,Probecard,Final_1,Final_2,PInit1,PTime1,PInit2,PTime2\n")

print total_time
for item in fileList :
    myfile = open(dirName + "/" + item,'r')
    dic = pickle.load(myfile)
    for key, value in dic.items() :
        if (re.search("Grip*",key)) :
            del dic[key]
    isReject = True
    isReject = selectChipCondition(dic,chipCondition)
    if isReject :
        print "REJECTED NOT SUITABLE DATA"
        continue
    print (dic)
    chipbychip_list = []
    chipbychip_list.insert(0,dic.get('trayID'))
    chipbychip_list.insert(1,dic.get('chipID'))
    chipbychip_list.insert(2,dic.get('chipOK'))
    chipbychip_list.insert(3,(dic.get('Finish') - dic.get('Start')).total_seconds())
    total_time.append((dic.get('Finish') - dic.get('Start')).total_seconds())

    if 'Dim' in dic :
        chipbychip_list.insert(4,(dic.get('Dim') - dic.get('Start')).total_seconds())
        tray_to_ppc.append((dic.get('Dim') - dic.get('Start')).total_seconds())
    else :
        chipbychip_list.insert(4,"***")

    if 'Edge' in dic :
        chipbychip_list.insert(5,(dic.get('Edge') - dic.get('Dim')).total_seconds())
        dimension_check.append((dic.get('Edge') - dic.get('Dim')).total_seconds())
        if 'fProbe' in dic :
            chipbychip_list.insert(6,(dic.get('fProbe') - dic.get('Edge')).total_seconds())
            edge_integrity.append((dic.get('fProbe') - dic.get('Edge')).total_seconds())
            if 'endProbe' in dic :
                chipbychip_list.insert(7,(dic.get('endProbe') - dic.get('fProbe')).total_seconds())
                probecard_measurement_total.append((dic.get('endProbe') - dic.get('fProbe')).total_seconds())
                chipbychip_list.insert(8,(dic.get('Finish') - dic.get('endProbe')).total_seconds())
                ppc_to_tray.append((dic.get('Finish') - dic.get('endProbe')).total_seconds())
                chipbychip_list.insert(9,"***")
            else :
                chipbychip_list.insert(7,"***")
                chipbychip_list.insert(8,(dic.get('Finish') - dic.get('fProbe')).total_seconds())
                ppc_to_tray.append((dic.get('Finish') - dic.get('fProbe')).total_seconds())
                chipbychip_list.insert(9,"***")
        else :
            chipbychip_list.insert(6,"***")
            chipbychip_list.insert(7,"***")
            chipbychip_list.insert(8,(dic.get('Finish') - dic.get('Edge')).total_seconds())
            chipbychip_list.insert(9,"***")

    else :
        if 'fProbe' in dic :
            chipbychip_list.insert(5,(dic.get('fProbe') - dic.get('Dim')).total_seconds())
            dimension_check.append((dic.get('fProbe') - dic.get('Dim')).total_seconds())
            chipbychip_list.insert(6,"***")
            if 'endProbe' in dic :
                chipbychip_list.insert(7,(dic.get('endProbe') - dic.get('fProbe')).total_seconds())
                probecard_measurement_total.append((dic.get('endProbe') - dic.get('fProbe')).total_seconds())
                chipbychip_list.insert(8,(dic.get('Finish') - dic.get('endProbe')).total_seconds())
                ppc_to_tray.append((dic.get('Finish') - dic.get('endProbe')).total_seconds())
                chipbychip_list.insert(9,"***")
            else :
                chipbychip_list.insert(7,"***")
                chipbychip_list.insert(8,(dic.get('Finish') - dic.get('fProbe')).total_seconds())
                ppc_to_tray.append((dic.get('Finish') - dic.get('fProbe')).total_seconds())
                chipbychip_list.insert(9,"***")

        else :
            chipbychip_list.insert(5,"***")
            chipbychip_list.insert(6,"***")
            chipbychip_list.insert(7,"***")
            chipbychip_list.insert(8,"***")
            chipbychip_list.insert(9,(dic.get('Finish') - dic.get('Dim')).total_seconds())
            
        

    if ('Probe0' in dic) :
        probecard_measurement_initialization_1st.append((dic.get('Probe0') - dic.get('fProbe')).total_seconds())
        chipbychip_list.insert(11,(dic.get('Probe0') - dic.get('fProbe')).total_seconds())
        if ('sProbe' in dic) :
            probecard_measurement_1st.append((dic.get('sProbe') - dic.get('Probe0')).total_seconds())
            chipbychip_list.insert(12,(dic.get('sProbe') - dic.get('Probe0')).total_seconds())
            if ('Probe1' in dic) :
                probecard_measurement_initialization_2nd.append((dic.get('Probe1') - dic.get('sProbe')).total_seconds())
                chipbychip_list.insert(13,(dic.get('Probe1') - dic.get('sProbe')).total_seconds())
                probecard_measurement_2nd.append((dic.get('endProbe') - dic.get('Probe1')).total_seconds())
                chipbychip_list.insert(14,(dic.get('endProbe') - dic.get('Probe1')).total_seconds())
        else :
            probecard_measurement_1st.append((dic.get('endProbe') - dic.get('Probe0')).total_seconds())
            chipbychip_list.insert(12,(dic.get('endProbe') - dic.get('Probe0')).total_seconds())

    strForPrint = str(dic.get('Start'))
    for item in chipbychip_list :
        strForPrint += ","
        strForPrint += str(item)
    strForPrint += "\n"
    fileChipbyChip.write(strForPrint)

analyze_process(total_time,chipCondition)
analyze_process(tray_to_ppc,chipCondition)
analyze_process(dimension_check,chipCondition)
analyze_process(edge_integrity,chipCondition)
analyze_process(probecard_measurement_total,chipCondition)
analyze_process(ppc_to_tray,chipCondition)
analyze_process(probecard_measurement_initialization_1st,chipCondition)
analyze_process(probecard_measurement_initialization_2nd,chipCondition)
analyze_process(probecard_measurement_1st,chipCondition)
analyze_process(probecard_measurement_2nd,chipCondition)
