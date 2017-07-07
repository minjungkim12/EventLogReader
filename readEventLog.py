import re
import os
from datetime import datetime, date
import time
from operator import itemgetter
import cPickle as pickle

def checkdatacondition(dic) :
    if not ('Start' in dic) :
        # print "cannot find start time of test"
        isContinue = False
        return isContinue
    if not ('Dim' in dic) :
        #        print "cannot find start time of dimension inspection"
        isContinue = False
        return isContinue
    if not ('Edge' in dic) :
        #        print "cannot find start time of Edge inspection"
        isContinue = False
        return isContinue
    if not ('fProbe' in dic) :
        #        print "cannot find start time of Frist Probecard measurement"
        isContinue = False
        return isContinue
    if not ('endProbe' in dic) :
        #        print "cannot find end time of Probecard measurement"
        isContinue = False
        return isContinue
    if not ('Finish' in dic) :
        #        print "cannot find end time of test"
        isContinue = False
        return isContinue
    isContinue = True
    return isContinue

dirName = './EventLog'
fileList = os.listdir(dirName)
lines=[]
for item in fileList :
    myfile = open(dirName + "/" + item,'r')
    for line in myfile:
        lines.append(line)
    myfile.close()

strNEW = re.compile("Move traypos \D\d to PPC",re.IGNORECASE)
strDim = re.compile("NOW Check dimensions: comment line skipped.")#Starting Dimension Inspection
strEdge = re.compile("NOW CHECK EDGE INTEGRITY: comment line skipped.")#Starting Edge Integrity 
strProbe1 = re.compile("Probecard First test started")#Start preparing ProbeCardMeasurement
strProbe2 = re.compile("Probecard Retest started..")#Starting ProbeCazrdMeasurement needles connection completed
strProbe = re.compile("Response: measure chip: command started")
strSTATUS = re.compile("Response: measure chip: command completed*",re.IGNORECASE) #"probecard measurement" finished ->will give chip status
strCHDO = re.compile("Response: CHDO ",re.IGNORECASE) #after "probecard measurement" and PPC->TRAY

strGrip = re.compile("Response: gripper contact program: command started, pick chip.")#gripper->chip

strTray = re.compile("TR\d") #string for tray ID
strChip = re.compile("\D\d") #string for chip position ID

strTime = re.compile("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d")

dic = {}
dic2 = {}
index = ""
counterG=0
counterP=0
thistrayID = ""
thischipID = ""
traytoppc = []
dimcheck = []
edgecheck = []
PCmeasure = []
ppctotray = []
totaltime = []

for line in lines:
    if type(line) is str :
        spltline = re.split('[="]+',line)
        for splits in spltline :
            isTime = strTime.match(splits)
            if (isTime) :
                thistime = datetime.strptime(splits,"%Y-%m-%d %H:%M:%S.%f")
                timestamp = thistime
                isNew = strNEW.search(line)
                isDim = strDim.search(line)
                isEdge = strEdge.search(line)
                isProbe = strProbe.search(line)
                isProbe1 = strProbe1.search(line)
                isProbe2= strProbe2.search(line)
                isStatus = strSTATUS.search(line)
                isInfo =strCHDO.search(line)
                isGrip = strGrip.search(line)
                
                if isNew :
                    counterG=0
                    counterP=0
                    dic.clear()
                    dic2.clear()
                    dic['Start']=timestamp
                
                if isDim :
                    dic['Dim']=timestamp

                if isEdge :
                    dic['Edge']=timestamp

                if isProbe1 :
                    dic['fProbe']=timestamp

                if isProbe2 :
                    dic['sProbe']=timestamp

                if isStatus :
                    dic['endProbe']=timestamp
                    dic['chipOK']=not (re.search("not",line))

                if isProbe :
                    dic["Probe"+str(counterP)]=timestamp
                    counterP+=1
               
                if isGrip :
                    dic["Grip"+str(counterG)]=timestamp
                    counterG+=1

                if isInfo :
                    dic['Finish']=timestamp
                    ssplits = re.split('[=" ]+',line)
                    for sssplits in ssplits :
                        trayID = strTray.match(sssplits)
                        chipID = strChip.match(sssplits)
                        if trayID :
                            dic['trayID'] = sssplits
                        if chipID :
                            dic['chipID'] = sssplits[0:2]

                    isContinue = checkdatacondition(dic)
                   
                    if(isContinue) :
                        filename = str(dic.get('trayID')) +  str(dic.get('chipID')) +"_"+(dic.get('Start')).strftime('%m%d%H%M')+".pkl"
                        output = open("./result/"+filename,'wb')
                        pickle.dump(dic,output)
                        output.close()
                    dic.clear()


