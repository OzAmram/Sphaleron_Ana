# Read NanoAOD and make smaller ttree for fitting & plotting


import ROOT
from ROOT import *
from array import array

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetSysColl import JetSysColl, JetSysObj
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import eventLoop
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim
from Sphaleron_Ana.NanoAODReader.CrabOutput import *

import pickle
import copy

def add_dict_to_tree(tree, d, label):
    #Add dictionary as branches to ttree
    for key in d.keys():
        tree.Branch(key, d[key], key+label)
    return tree





def NanoReader(inputFileName="in.root", outputFileName="out.root", cut=None, nJobs = 1, jobNum = 1, json = None):

    inputFile = TFile.Open(inputFileName)
    if(not inputFile): #check for null pointer
        print("Unable to open file %s, exting \n" % inputFileName)
        return 1

    #get input tree
    inTree = inputFile.Get("Events")
    # pre-skimming
    elist,jsonFilter = preSkim(inTree, json, cut)

    #number of events to be processed 
    nTotal = elist.GetN() if elist else inTree.GetEntries()
    
    print 'Pre-select %d entries out of %s '%(nTotal,inTree.GetEntries())


    inTree= InputTree(inTree, elist) 


    # Grab event tree from nanoAOD
    eventBranch = inTree.GetBranch('event')
    treeEntries = eventBranch.GetEntries()

    # Design the splitting if necessary
    #if nJobs != 1:
    #    evInJob = int(treeEntries/nJobs)

    #    lowBinEdge = evInJob*(jobNum-1)
    #    highBinEdge = evInJob*jobNum

    #    if jobNum == nJobs:
    #        highBinEdge = treeEntries
    #else:
    #    lowBinEdge = 0
    #    highBinEdge = treeEntries

    #print "Range of events: (" + str(lowBinEdge) + ", " + str(highBinEdge) + ")"

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

    outputFile = TFile(outputFileName, "recreate")

    outTree = TTree("Events", "Events")
    outTree = add_dict_to_tree(outTree, tout_floats, "/F")
    outTree = add_dict_to_tree(outTree, tout_ints, "/I")

    crabOutput= CrabOutput(inputFile, inTree, outputFile, outTree, provenance=True, jsonFilter = jsonFilter)

    min_pt = 70.
    count = 0



# -------- Begin Loop-------------------------------------
    entries = inTree.entries
    for entry in xrange(entries):

        count   =   count + 1
        if count % 10000 == 0 :
            print  '--------- Processing Event ' + str(count) +'   -- percent complete ' + str(100*count/nTotal) + '% -- '

        # Grab the event
        event = Event(inTree, entry)



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


        trigger = (int) (inTree.readBranch('HLT_PFHT900') or inTree.readBranch('HLT_PFHT800'))
        Weight = inTree.readBranch('genWeight')

        AK4JetsCol = Collection(event, "Jet")
        MuonsCol = Collection(event, "Muon")
        ElectronsCol = Collection(event, "Electron")
        PhotonsCol = Collection(event, "Photon")
        MET = inTree.readBranch('MET_pt')

        jets= set()
        mus = set()
        els = set()
        phots = set()
        R_min = 0.3
        for jet in AK4JetsCol:
            #jetId : bit1 = loose, bit2 = tight, bit3 = tightLepVeto
            #want loose id
            if((jet.jetId % 2 == 1) and jet.pt > min_pt):
                jets.add(jet.p4())
        for mu in MuonsCol:
            if(mu.tightId and abs(mu.eta) < 2.4 and mu.pt > min_pt):
                mus.add(mu.p4())

        for el in ElectronsCol:
            #cut based id: 0 = fail, 1 = veto, 2 = loose, 3 = medium , 4 = tight
        #want medium id
            if(el.cutBased >= 3 and abs(el.eta) < 2.5 and el.pt > min_pt):
                els.add(el.p4())

        for phot in PhotonsCol:
            #cut based id: 0 = fail, 1 = veto, 2 = loose, 3 = medium , 4 = tight
            #want medium id
            if( phot.cutBased >=3 and abs(phot.eta) < 2.5 and phot.pt > min_pt):
                phots.add(phot.p4())

        jets_to_remove = set()
        els_to_remove = set()
        phots_to_remove = set()

        # Cleanup overlapping jets
        for jet in jets:
            for el in els:
                if(jet.DeltaR(el) < R_min):
                    if((el.Et()/jet.Et()) > 0.7):
                        jets_to_remove.add(jet)
                    else:
                        els_to_remove.add(el)
            for mu in mus:
                if(jet.DeltaR(mu) < R_min):
                    if((mu.Et()/jet.Et()) > 0.8):
                        jets_to_remove.add(jet)
            for phot in phots:
                if(jet.DeltaR(phot) < R_min):
                    if((phot.Et()/jet.Et()) > 0.5):
                        jets_to_remove.add(jet)
                    else:
                        phots_to_remove.add(phot)
             
        #cleanup overlapping photons and leptons
        for phot in phots:
            for el in els:
                if(phot.DeltaR(el) < R_min):
                    phots_to_remove.add(phot)
            for mu in mus:
                if(phot.DeltaR(mu) < R_min):
                    phots_to_remove.add(phot)
        for el in els:
            for mu in mus:
                if(el.DeltaR(mu) < R_min):
                    els_to_remove.add(el)
        
        #do the removal
        for jet in jets_to_remove:
            jets.remove(jet)
        for el in els_to_remove:
            els.remove(el)
        for phot in phots_to_remove:
            phots.remove(phot)


        for jet in jets:
            ST += jet.Et()
            HT += jet.Et()
            NJets += 1
            Event_vector += jet
        for mu in mus:
            ST += mu.Et()
            Mu_Pt += mu.Et()
            NMus += 1
            Event_vector += mu

        for el in els:
            ST += el.Et()
            El_Pt += el.Et()
            NEls += 1
            Event_vector += el

        for phot in phots:
            ST += phot.Et()
            Event_vector += phot

        Mass = Event_vector.M()

        Float_dict= {
                "ST":ST,
                "MET":MET,
                "HT":HT,
                "Mu_Pt":Mu_Pt,
                "El_Pt":El_Pt,
                "Mass":Mass,
                "Weight":Weight
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

        outTree.Fill()

    crabOutput.Write()
    return count




