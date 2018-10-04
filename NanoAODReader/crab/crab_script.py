
#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.framework.jobreport import JobReport
from Sphaleron_Ana.NanoAODReader.NanoReader import * 

nFiles = 0
outFilesList = []
jobReport = JobReport()
for f in inputFiles():
    nFiles+=1
    outStr = "out" + str(nFiles)
    outFilesList.append(outStr)
    nEvents = NanoReader(inputFileName = f, outputFileName=outStr, nJobs=1, jobNum=1, json=runsAndLumis())
    print("events are %i \n" %nEvents)
    jobReport.addInputFile(f,nEvents)

#hadd outputs
hadd_cmnd = "./haddnano.py tree.root "
for f in outFilesList:
    hadd_cmnd += f + " "

print("executing : %s" % hadd_cmnd)
os.system(hadd_cmnd)
print("ls")
os.system("ls")



jobReport.addOutputFile("tree.root")
jobReport.save()

print "DONE"
os.system("ls -lR")


