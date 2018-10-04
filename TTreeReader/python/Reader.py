
import ROOT
from ROOT import TBranch, TTree
from array import array
import pickle
import copy


class TTreeReader:
    """Class to help read from TTrees """
    def __init__(self, inFile):
        self.inFile = inFile
        self.tree = inFile.Get("Events")
        self.nEvents = self.tree.GetEntries()
        self.branchList = self.tree.GetListOfBranches()
        self.nBranches = self.branchList.GetEntries()
        self.vals = {}
        for i in xrange(self.nBranches):
            branch = self.branchList.At(i)
            name = branch.GetName()
            print("Adding branch %s \n", name)
            if(branch.GetTitle()[-1] == 'F'):
                #float type
                self.vals[name] = 0.
            elif(branch.GetTitle()[-1] == 'I'):
                #float type
                self.vals[name] = 0
            else:
                print("Can't parse Branch %s with label %s, not a float or int \n" %(name, branch.GetTitle()))
        
        self.normalization = 1.

    def setNorm(self, xsec):
        #setup normalization of the sample
        runs = self.inFile.Get("Runs")
        runs.GetEntry(0)
        totWeight = runs.genEventSumw
        self.normalization = xsec/totWeight




    def getEvent(self, i):
        self.tree.GetEntry(i)
        for key in self.vals.keys():
            self.vals[key] = self.tree.__getattr__(key)
        return None


