
#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from NanoReader import * 

nFiles = 0
outFilesList = []
for f in inputFiles():
    nFiles+=1
    outStr = "out" + str(nFiles)
    outFilesList.append(outStr)
    NanoReader(inputFile = f, outputFile=outStr)

#hadd outputs
hadd_cmnd = "hadd NanoOut.root "
for f in outFilesList:
    hadd_cmnd += f + " "

print("ls")
os.system("ls")
print("executing : %s" % hadd_cmnd)
os.system(hadd_cmnd)





