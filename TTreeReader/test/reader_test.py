
import ROOT
from ROOT import TFile, TCanvas
from Sphaleron_Ana.TTreeReader.Reader import *
from Sphaleron_Ana.TTreeReader.HistMaker import *

def run():
    ROOT.gROOT.SetBatch(True)
    f1 = TFile.Open("../../NanoAODReader/tree_1.root")
    print("Open file \n")
    if(not f1):
        print("Can't open file \n");
        return 1;
    ttr = TTreeReader(f1)
    ttr.setNorm(7.6)
    ttr.getEvent(1)
    print("ST for event 1 is %s \n" % ttr.vals["ST"])
    c = TCanvas("c0", "", 0,0, 800, 800)
    h_ST = simpleHistMaker(ttr, "ST", "ST; ST (GeV)", 100, 1000., 15000. )
    h_ST.Draw("hist")
    print("h integral is %.2f \n" % (h_ST.Integral()))
    c.SaveAs("Sphaleron_ST_test.pdf")

run()
