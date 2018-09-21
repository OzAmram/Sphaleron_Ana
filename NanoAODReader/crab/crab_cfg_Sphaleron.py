
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'Sphaleron'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['../NanoReader.py', 'crab_script.py', 'crab_script_jetNano.py', 'keep_and_drop_jetNano.txt', '../../../../PhysicsTools/NanoAODTools/scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.disableAutomaticOutputCollection = True
config.JobType.outputFiles = ["NanoOut.root"]
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/Sphaleron_NNPDF30_lo_as_0118_0_pythia8TuneCUETP8M1/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 5
#config.Data.totalUnits = 2000
config.Data.splitting = 'FileBased'
config.Data.runRange = ''
config.Data.lumiMask  = ''
config.Data.outLFNDirBase = '/store/user/oamram/NTuples/Sphal/'
config.Data.publication = False
config.Data.outputDatasetTag = 'Sphaleron'
config.section_("Site")
config.Site.storageSite = "T3_US_FNALLPC"

