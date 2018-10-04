#wrapper to output root files to crab correctly

from PhysicsTools.NanoAODTools.postprocessing.framework.output import *
class CrabOutput(OutputTree):
    def __init__(
            self,
            inputFile,
            inputTree,
            outputFile,
            outputTree,
            provenance=False,
            jsonFilter=None
    ):
        outputFile.cd()


        OutputTree.__init__(self, outputFile, outputTree, inputTree)
        self._inputTree = inputTree
        self._otherTrees = {}
        self._otherObjects = {}
        for k in inputFile.GetListOfKeys():
            kn = k.GetName()
            if kn == "Events":
                continue # this we are doing
            elif kn in ("MetaData", "ParameterSets"):
                if provenance: self._otherTrees[kn] = inputFile.Get(kn).CopyTree('1')
            elif kn in ("LuminosityBlocks", "Runs"):
                if not jsonFilter: self._otherTrees[kn] = inputFile.Get(kn).CopyTree('1')
                else:
                    _isRun = (kn=="Runs")
                    _it = inputFile.Get(kn)
                    _ot = _it.CloneTree(0)
                    for ev in _it:
                        if (jsonFilter.filterRunOnly(ev.run) if _isRun else jsonFilter.filterRunLumi(ev.run,ev.luminosityBlock)): _ot.Fill()
                    self._otherTrees[kn] = _ot
            elif k.GetClassName() == "TTree":
                print "Not copying unknown tree %s" % kn
            else:
                self._otherObjects[kn] = inputFile.Get(kn)
    def Write(self):
        OutputTree.write(self)
        for t in self._otherTrees.itervalues():
            t.Write()
        for on,ov in self._otherObjects.iteritems():
            self._file.WriteTObject(ov,on)
        self._file.Close()

