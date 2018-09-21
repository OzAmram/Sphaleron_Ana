#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
p=PostProcessor(".",inputFiles(),"(Jet_pt[0]>2000)&&(Jet_pt[1]>2000)",branchsel='keep_and_drop_jetNano.txt',modules=[jetmetUncertainties2016AK8PuppiNoGroom(),jetmetUncertainties2016AK4Puppi()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
p.run()

print "DONE"
os.system("ls -lR")

