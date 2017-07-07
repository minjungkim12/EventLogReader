# EventLogReader
EventLogReader_for_PNUINHA

Simple python scripts for ALICIA "EventLog" analysis

How To Use (basic) :
1. Put "EventLogxxxxx.txt" you want to analyze into EventLog directory.
2. run readEventLog.py -> **python readEventLog.py**
   this script generates the "pkl files" containing chip by chip info. under the **result** directory.
3. run analysisEventLog.py -> **python analysisEventLog.py"**
   this script generates the **"chipbychip_result.dat"** containing chip by chip info. in csv format and some basic plots under the **plots** directory.
   If you want to draw the result plots only for specific dataset, **modify analysisEventLog.py**


