
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'TEMPNAME'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['../python/NanoReader.py', 'crab_script.py', 'haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = 'TEMPINPUT'
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
config.Data.outputDatasetTag = 'TEMPNAME'
config.section_("Site")
config.Site.storageSite = "T3_US_FNALLPC"

