import subprocess
import pickle
from optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('--submit', action="store_true",
            default   =   False,
            dest      =   'submit',
            help      =   'Runs crab on everything')
    parser.add_option('--status', action="store_true",
            default   =   False,
            dest      =   'status',
            help      =   'Runs crab status for everything')
    parser.add_option('--setup', action="store_true",
            default   =   False,
            dest      =   'setup',
            help      =   'Runs setup for everything by making dictionary of samples')
    parser.add_option('--hadd', action="store_true",
            default   =   False,
            dest      =   'hadd',
            help      =   'Runs haddnano.py on everything')
    parser.add_option('--addLocations', action="store_true",
            default   =   False,
            dest      =   'addLocations',
            help      =   'Adds locations of hadded files to info')

    (options, args) = parser.parse_args()

    samplesFile = 'samplesInfo.p'

    try:
        input_subs = pickle.load(open(samplesFile,'rb'))
        do_setup = False
    except:
        do_setup = True

    if options.setup or do_setup:
        input_subs = {
                "Sphaleron": {"das" : "/Sphaleron_NNPDF30_lo_as_0118_0_pythia8TuneCUETP8M1/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName":"Sphaleron_NNPDF30_lo_as_0118_0_pythia8TuneCUETP8M1",
                    "histName": "Sphaleron",
                    "Nevents": 99999,
                    "xsec": 0.0101},

                "ttbar": {  "das": "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName": "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8",
                    "histName": "TTbar",
                    "Nevents": 75311946,
                    "xsec": 831.76},

                "QCD_Pt_1000to14000" : { "das": "/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName": "QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8",
                    "histName": "QCD",
                    "Nevents":  2999069,
                    "xsec": 9.4183 },
                "QCD_Pt_1400to1800" : { "das": "/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName": "QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8",
                    "histName": "QCD",
                    "Nevents":  396409,
                    "xsec": 0.84265 },
                "QCD_Pt_1800to2400" : { "das": "/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName": "QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8",
                    "histName": "QCD",
                    "Nevents":  397660,
                    "xsec": 0.114943},
                "QCD_Pt_2400to3200" : { "das": "/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName": "QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8",
                    "histName": "QCD",
                    "Nevents":  399226,
                    "xsec": 0.00682981},
                "QCD_Pt_3200toinf" : { "das": "/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName": "QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8",
                    "histName": "QCD",
                    "Nevents":  391735,
                    "xsec": 0.000165445},


                "ZJets_Pt_400to650" : {"das": "/DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/NANOAODSIM",
                    "requestName": "DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
                    "histName": "Z+Jets",
                    "Nevents": 1050705,
                    "xsec": 0.2816},
                "ZJets_Pt_650toInf" : {"das": "/DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/NANOAODSIM",
                    "requestName": "DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
                    "histName": "Z+Jets",
                    "Nevents": 1022595,
                    "xsec": 0.02639},


                "WJets_HT_800to1200" : {"das": "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName": "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "histName": "W+Jets",
                    "Nevents": 15445153,
                    "xsec": 5.501},
                "WJets_HT_1200to2500" : {"das": "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                    "requestName": "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "histName": "W+Jets",
                    "Nevents": 244532,
                    "xsec": 1.329},
                "WJets_HT_2500toInf" : {"das": "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM",
                        "requestName": "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                        "histName": "W+Jets",
                        "Nevents": 253561,
                        "xsec": 0.03216},

                }
        print("Doing setup. Dumping samples info to %s \n" % samplesFile)
        pickle.dump(input_subs,open(samplesFile,'wb'))



    if options.status:
        commands = []
        for set_name in input_subs.keys():
            commands.append('crab status crab_'+set_name)

        for s in commands:
            print 'Executing ' + s
            subprocess.call([s],shell=True)

    elif options.submit:
        commands = []
        for set_name in input_subs.keys():
            if set_name.find('data') != -1:     # if data
                commands.append("sed 's$TEMPNAME$"+set_name+"$g' templates/crab_cfg_data_template.py > crab_input/crab_cfg_"+set_name+".py")
            else:
                commands.append("sed 's$TEMPNAME$"+set_name+"$g' templates/crab_cfg_mc_template.py > crab_input/crab_cfg_"+set_name+".py")

            commands.append("sed -i 's$TEMPINPUT$"+input_subs[set_name]['das'] +"$g' crab_input/crab_cfg_"+set_name+".py")
            commands.append("crab submit -c crab_input/crab_cfg_"+set_name+".py")
            commands.append("mv crab_"+set_name +" crab_input")

        for s in commands:
            print 'Executing ' + s
            subprocess.call([s],shell=True)

    elif options.hadd or options.addLocations:
        myEosDir = '/eos/uscms/store/user/oamram/NTuples/Sphal/'

        commands = []
        for set_name in input_subs.keys():
            firstDir = input_subs[set_name]["requestName"] +"/"
            secondDir = set_name+"/"

            outputFile = myEosDir+'combined/'+set_name+'.root'

            # Pickle dictionary with set names
            input_subs[set_name]['location'] = outputFile

            if(options.hadd):
                commands.append('python haddnano.py '+ outputFile + ' ' + '`./get_crab_file_list.sh ' +myEosDir +firstDir + secondDir + '`')

        print("Adding hadded sample locations to %s \n" % samplesFile)
        pickle.dump(input_subs,open(samplesFile,'wb'))

        for s in commands:
            print 'Executing ' + s
            subprocess.call([s],shell=True)
