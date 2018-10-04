from ROOT import kBlue, TH1F
from Sphaleron_Ana.TTreeReader.Reader import *

def simpleHistMaker(treeR, var, title, nBins, binLow, binHigh, color=kBlue, lumi = 36.):
    #pass a TTreeReader and a string specifying the variable you want and make a histogram
    #normalization 
    h = TH1F(title, title, nBins, binLow, binHigh)
    for i in xrange(treeR.nEvents):
        treeR.getEvent(i)
        h.Fill(treeR.vals[var], lumi * treeR.normalization * 1)
    h.SetFillColor(color)
    h.SetLineColor(color)
    return h

