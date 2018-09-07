# Read NanoAOD and make smaller ttree for fitting & plotting


import ROOT
from ROOT import *
from array import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetSysColl import JetSysColl, JetSysObj

import pickle
from optparse import OptionParser
import copy

def add_dict_to_tree(tree, d, label):
#Add dictionary as branches to ttree
    for key in d.keys():
        tree.Branch(key, d[key], key+label)
    return tree




if __name__ == "__main__":
    
    parser = OptionParser()

    parser.add_option('-i', '--inputfile', metavar='F', type='string', action='store',
                    default   =   'test.root',
                    dest      =   'inputfile',
                    help      =   'input dataset')

    parser.add_option('-o', '--outputfile', metavar='F', type='string', action='store',
                    default   =   'out.root',
                    dest      =   'outputfile',
                    help      =   'input dataset')

    parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                    default   =   'data',
                    dest      =   'set',
                    help      =   'dataset (ie data,ttbar etc)')

    parser.add_option('-g', '--grid', metavar='F', type='string', action='store',
                    default   =   'off',
                    dest      =   'grid',
                    help      =   'running on grid off or on')
    parser.add_option('-m', '--modulesuffix', metavar='F', type='string', action='store',
                    default   =   'none',
                    dest      =   'modulesuffix',
                    help      =   'ex. PtSmearUp')
    parser.add_option('-n', '--num', metavar='F', type='string', action='store',
                    default   =   'all',
                    dest      =   'num',
                    help      =   'job number')
    parser.add_option('-j', '--jobs', metavar='F', type='int', action='store',
                    default   =   1,
                    dest      =   'jobs',
                    help      =   'number of jobs')
    parser.add_option('-S', '--split', metavar='F', type='string', action='store',
                    default   =   'file',
                    dest      =   'split',
                    help      =   'split by event of file') #EVENT SPLITTING DOESN'T CURRENTLY WORK

    (options, args) = parser.parse_args()

    fin = TFile.Open(options.inputfile)

    tree = fin.Get("Events")
    tree = InputTree(tree)

    # Grab event tree from nanoAOD
    eventBranch = tree.GetBranch('event')
    treeEntries = eventBranch.GetEntries()

    # Design the splitting if necessary
    jobs = options.jobs
    if jobs != 1:
        evInJob = int(treeEntries/jobs)
        
        lowBinEdge = evInJob*(num-1)
        highBinEdge = evInJob*num

        if num == jobs:
            highBinEdge = treeEntries
    else:
        lowBinEdge = 0
        highBinEdge = treeEntries

    print "Range of events: (" + str(lowBinEdge) + ", " + str(highBinEdge) + ")"

    tout_floats= {
            'ST':array('f', [0.]),
            'HT':array('f', [0.]),
            'MET':array('f', [0.]),
            'Mu_Pt':array('f', [0.]),
            'El_Pt':array('f', [0.]),
            'Mass':array('f', [0.]),
            'Weight':array('f', [0.])
            }

    tout_ints = {
            'trigger':array('i', [0]),
            'NJets':array('i', [0]),
            'NMus':array('i', [0]),
            'NEls':array('i', [0])
            }

    fout = TFile(options.outputfile, "recreate")

    tout = TTree("tout", "tout")
    tout = add_dict_to_tree(tout, tout_floats, "/F")
    tout = add_dict_to_tree(tout, tout_ints, "/I")

    min_pt = 70.
    count = 0



# -------- Begin Loop-------------------------------------
    for entry in range(lowBinEdge,highBinEdge):

        count   =   count + 1
        if count % 10000 == 0 :
            print  '--------- Processing Event ' + str(count) +'   -- percent complete ' + str(100*count/(highBinEdge-lowBinEdge)) + '% -- '

        # Grab the event
        tree.GetEntry(entry)
        event = Event(tree, entry)
        #event = tree.event



        ST = 0.
        MET = 0.
        HT = 0. 
        Mu_Pt = 0.
        El_Pt = 0.
        Mass = 0.
        NJets = 0
        NMus = 0
        NEls = 0
        Event_vector = ROOT.TLorentzVector()


        trigger = (int) (tree.HLT_PFHT900 or tree.HLT_PFHT800)
        weight = tree.genWeight

        AK4JetsCol = Collection(event, "Jet")
        MuonsCol = Collection(event, "Muon")
        ElectronsCol = Collection(event, "Electron")
        PhotonsCol = Collection(event, "Photon")
        MET = tree.MET_pt

        for jet in AK4JetsCol:
            #jetId : bit1 = loose, bit2 = tight, bit3 = tightLepVeto
            #want loose id
            if((jet.jetId % 2 == 1) and jet.pt > min_pt):
                ST += jet.pt
                HT += jet.pt
                NJets += 1
                Event_vector += jet.p4()
        for mu in MuonsCol:
            if(mu.tightId and abs(mu.eta) < 2.4 and mu.pt > min_pt):
                ST += mu.pt
                Mu_Pt += mu.pt
                NMus += 1
                Event_vector += mu.p4()

        for el in ElectronsCol:
        #cut based id: 0 = fail, 1 = veto, 2 = loose, 3 = medium , 4 = tight
        #want medium id
            if(el.cutBased >= 3 and abs(el.eta) < 2.5 and el.pt > min_pt):
                ST += el.pt
                El_Pt += el.pt
                NEls += 1
                Event_vector += el.p4()

        for phot in PhotonsCol:
        #cut based id: 0 = fail, 1 = veto, 2 = loose, 3 = medium , 4 = tight
            #want medium id
            if( phot.cutBased >=3 and abs(phot.eta) < 2.5 and phot.pt > min_pt):
                ST += phot.pt
                Event_vector += phot.p4()
    
        Mass = Event_vector.M()

        Float_dict= {
                "ST":ST,
                "MET":MET,
                "HT":HT,
                "Mu_Pt":Mu_Pt,
                "El_Pt":El_Pt,
                "Mass":Mass
                }


        Int_dict = {
                "trigger":trigger,
                "NJets":NJets,
                "NMus":NMus,
                "NEls":NEls,
                }
        for key in Int_dict.keys():
            tout_ints[key][0] = Int_dict[key]

        for key in Float_dict.keys():
            tout_floats[key][0] = Float_dict[key]
    
        tout.Fill()
    
    fout.Write()
    fout.Close()



    
