
#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.framework.jobreport import JobReport
from NanoReader import * 

nFiles = 0
outFilesList = []
jobReport = JobReport()
for f in inputFiles():
    nFiles+=1
    outStr = "out" + str(nFiles)
    outFilesList.append(outStr)
    nEvents = NanoReader(inputFile = f, outputFile=outStr)
    jobReport.addInputFile(f,nEvents)

#hadd outputs
hadd_cmnd = "hadd NanoOut.root "
for f in outFilesList:
    hadd_cmnd += f + " "

print("executing : %s" % hadd_cmnd)
os.system(hadd_cmnd)
print("ls")
os.system("ls")



jobReport.addOutputFile("NanoOut.root")
jobReport.save()


