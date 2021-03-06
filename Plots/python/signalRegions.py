'''
Get a signal region plot from the fitDiagnostics workspace
'''

#!/usr/bin/env python
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--signal",               dest='signal',  action='store', default='T2tt',    choices=["T2tt", "T2bW", "ttHinv"], help="which signal?")
parser.add_option("--massPoints",           dest='massPoints',  action='store', default='800_100,350_150', help="which masspoints??")
parser.add_option("--version",              dest='version', action='store', default='v8',    help="Which version of estimates should be used?")
parser.add_option('--logLevel',             dest="logLevel",              default='INFO',              action='store',      help="log level?", choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'])
parser.add_option('--blinded',              action="store_true")
parser.add_option('--postFit',              dest="postFit", default = False, action = "store_true", help="Apply pulls?")
parser.add_option('--expected',             action = "store_true", help="Run expected?")
parser.add_option('--preliminary',          action = "store_true", help="Run expected?")
parser.add_option('--testGrayscale',        action = "store_true", help="Do the most important test for this collaboration?")
parser.add_option("--postFix",              action='store',      default="", help='Add sth?')
(options, args) = parser.parse_args()

# Standard imports
import ROOT
import os
import sys
import pickle
import math
import yaml

# Analysis
from WH_studies.Tools.u_float           import u_float
from WH_studies.Tools.asym_float           import asym_float as af
from WH_studies.Tools.getPostFit        import *

regions = range(12)

from RootTools.core.standard import *
# logger
import WH_studies.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   options.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None)

lumiStr = 137

isData = True if not options.expected else False
massPoints = options.massPoints.split(',')

#workspace  = 'data/fitDiagnostics_750_1.root'
workspace  = 'data/fitDiagnostics_800_100.root'
workspace2 = 'data/fitDiagnostics_425_150.root'
workspace3 = 'data/fitDiagnostics_225_75.root'

# get the results
postFitResults = getPrePostFitFromMLF(workspace)
postFitResults2 = getPrePostFitFromMLF(workspace2)
postFitResults3 = getPrePostFitFromMLF(workspace3)
covariance = getCovarianceFromMLF(workspace, postFit=options.postFit)

preFitHist={}
postFitHist={}
bhistos=[]
hists={}
histos={}
bkgHist=[]
processes = [('top', 't#bar{t}/single t'),
            ('wjets', 'W+jets'),
            ('other', 'SM WH'),
            ('total_background', 'total'), # for uncertainties
            ('data', 'Total'),
            ('sig', 'TChiWH(800,100)'),
            #('sig', 'TChiWH(750,1)'),
            ('sig2', 'TChiWH(425,150)'),
            ('sig3', 'TChiWH(225,75)'),\
            ]

## need to sort the regions somehow
#regions = postFitResults['hists']['shapes_prefit'].keys()
regions = [\
    ('nj2_lowmet_res',   2, 0, '125--200'),
    ('nj2_medmet_res',   2, 0, '200--300'),
    ('nj2_highmet_res',  2, 0, '300--400'),
    ('nj2_vhighmet_res', 2, 0, '$>400$'),
    ('nj2_lowmet_boos',  2, 1, '125--300'),
    ('nj2_medmet_boos',  2, 1, '$>300$'),
    ('nj3_lowmet_res',   3, 0, '125--200'),
    ('nj3_medmet_res',   3, 0, '200--300'),
    ('nj3_highmet_res',  3, 0, '300--400'),
    ('nj3_vhighmet_res', 3, 0, '$>400$'),
    ('nj3_lowmet_boos',  3, 1, '125--300'),
    ('nj3_medmet_boos',  3, 1, '$>300$')
    ]


hists = { p:ROOT.TH1F(p,tex,len(regions),0,len(regions)) for p,tex in processes }

shapes = 'shapes_prefit' if not options.postFit else 'shapes_fit_s'

res = []

dict_for_table = []
for ibin, region in enumerate(regions):
    binName, nJet, nHiggs, MET = region
    row = {'MET':MET, 'nJet':nJet, 'nHiggs':nHiggs, 'wjets':0, 'top':0, 'other':0, 'total_background':0, 'sig':0, 'sig2':0, 'sig3':0, 'data':0}
    dict_for_table.append(row)
    res.append(row)

for p,tex in processes:
    hists[p].legendText = tex
    for ibin, region in enumerate(regions):
        binName, nJet, nHiggs, MET = region
        shapesKey = 'shapes_prefit' if p.count('sig') else shapes
        if p == 'data':
            pred = int(round(postFitResults['hists'][shapesKey][binName][p].Eval(1),0))
            #hists[p].SetBinContent(ibin+1, obs)
            #hists[p].SetBinError(ibin+1, af(obs)
        elif p == 'sig2':
            try:
                pred = postFitResults2['hists'][shapesKey][binName]['sig'].GetBinContent(1)
                err  = postFitResults2['hists'][shapesKey][binName]['sig'].GetBinError(1)
            except KeyError:
                pred, err = 0, 0
        elif p == 'sig3':
            try:
                pred = postFitResults3['hists'][shapesKey][binName]['sig'].GetBinContent(1)
                err  = postFitResults3['hists'][shapesKey][binName]['sig'].GetBinError(1)
            except KeyError:
                pred, err = 0, 0
        else:
            try:
                pred = postFitResults['hists'][shapesKey][binName][p].GetBinContent(1)
                err  = postFitResults['hists'][shapesKey][binName][p].GetBinError(1)
            except KeyError:
                pred, err = 0, 0

        hists[p].SetBinContent(ibin+1, pred)
        if not p == 'data':
            hists[p].SetBinError(ibin+1, err)

        if pred<0.01:
            pred_str = '$<0.01$'
        elif pred<0.1:
        #elif p=='other':
            pred_str = "${:.2f} \pm {:.2f}$".format(pred, err)
        else:
            pred_str = "${:.2f} \pm {:.2f}$".format(pred, err)
        dict_for_table[ibin][p] = pred_str
        res[ibin][p] = pred

colors = {'top':ROOT.kAzure+6, 'wjets':ROOT.kGreen+1, 'other':ROOT.kRed-2}

hists['top'].style = styles.fillStyle(ROOT.kAzure+6)
hists['wjets'].style = styles.fillStyle(ROOT.kGreen+1)
hists['other'].style = styles.fillStyle(ROOT.kRed-2)
hists['sig'].style = styles.lineStyle(ROOT.kBlack, width=3)
hists['sig2'].style = styles.lineStyle(ROOT.kBlack, width=3, dashed=True)
hists['sig3'].style = styles.lineStyle(ROOT.kBlack, width=3, dotted=True)
hists['data'].SetBinErrorOption(ROOT.TH1F.kPoisson)
hists['data'].style = styles.errorStyle( ROOT.kBlack, markerSize = 1., drawOption='e0' )

ymin = 0.006

boxes = []
ratio_boxes = []

for ib, region in enumerate(regions):
    binName, nJet, nHiggs, MET = region
    val = hists['total_background'].GetBinContent(ib+1)
    sys = hists['total_background'].GetBinError(ib+1)
    sys_rel = sys/val
    print "Bin {:25} pred: {:.3} +/- {:.3}, obs: +/-".format(binName, val, sys)
    box = ROOT.TBox( hists['total_background'].GetXaxis().GetBinLowEdge(ib+1),  max([ymin, val-sys]), hists['total_background'].GetXaxis().GetBinUpEdge(ib+1), max([ymin, val+sys]) )
    box.SetLineColor(ROOT.kGray+1)
    box.SetFillStyle(3244)
    box.SetFillColor(ROOT.kGray+1)
    boxes.append(box)

    r_box = ROOT.TBox( hists['total_background'].GetXaxis().GetBinLowEdge(ib+1),  max(0.11, 1-sys_rel), hists['total_background'].GetXaxis().GetBinUpEdge(ib+1), min(1.9, 1+sys_rel) )
    r_box.SetLineColor(ROOT.kGray+1)
    r_box.SetFillStyle(3244)
    r_box.SetFillColor(ROOT.kGray+1)
    ratio_boxes.append(r_box)


binLabels = ['','200','300','400','','300','','200','300','400','','300','']
def setBinLabels( hist ):
    for i in range(1, hist.GetNbinsX()+1):
        hist.GetXaxis().SetBinLabel(i, '%s        '%binLabels[i-1])

def drawDivisions(regions):
    # divisions in main plot
    min = 0.15
    max = 0.95
    diff = (max-min) / len(regions)
    lines = []
    lines2 = []
    line = ROOT.TLine()
    line.SetLineWidth(1)
    line.SetLineStyle(2)
    lines  = [ (min+4*diff,  0.005, min+4*diff, 0.84) ]
    lines += [ (min+6*diff,  0.005, min+6*diff, 0.90) ]
    lines += [ (min+10*diff,  0.005, min+10*diff, 0.84) ]
    return [line.DrawLineNDC(*l) for l in lines] + [tex.DrawLatex(*l) for l in []] + [tex2.DrawLatex(*l) for l in lines2]

def drawDivisionsRatio(regions):
    # divisons in ratio plot
    min = 0.15
    max = 0.95
    diff = (max-min) / len(regions)
    lines = []
    lines2 = []
    line = ROOT.TLine()
    line.SetLineWidth(1)
    line.SetLineStyle(2)
    lines  = [ (min+4*diff,  0.45, min+4*diff, 0.90) ]
    lines += [ (min+6*diff,  0.45, min+6*diff, 0.90) ]
    lines += [ (min+10*diff, 0.45, min+10*diff, 0.90) ]
    return [line.DrawLineNDC(*l) for l in lines] + [tex.DrawLatex(*l) for l in []] + [tex2.DrawLatex(*l) for l in lines2]

def drawTexLabels( regions ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.042)
    tex.SetTextAngle(0)
    tex.SetTextAlign(12) # align right
    min = 0.15
    max = 0.95
    diff = (max-min) / len(regions)
    lines  = [ (min + (7./2)*diff-0.02, 0.87, "#bf{N_{jets} = 2}"), (min + (3./2)*diff, 0.82, "#bf{N_{H} = 0}"), (min + (9./2)*diff, 0.82, "#bf{N_{H} = 1}") ] 
    lines += [ (min + (19./2)*diff-0.02, 0.87, "#bf{N_{jets} = 3}"), (min + (15./2)*diff, 0.82, "#bf{N_{H} = 0}"), (min + (21./2)*diff, 0.82, "#bf{N_{H} = 1}")] 
    return [tex.DrawLatex(*l) for l in lines]

def getLegend():
    leg = ROOT.TLegend(0.17,0.75-8*0.045, 0.38, 0.75)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.040)
    for p,tex in processes:
        if p.count('sig') or p=='data' or p=='total_background': continue
        hists[p].SetFillColor(colors[p])
        hists[p].SetLineColor(colors[p])
        leg.AddEntry(hists[p], '#bf{%s}'%tex, 'f' )
    hists['sig'].SetLineColor(1)
    hists['sig'].SetLineWidth(2)
    hists['sig'].SetLineStyle(1)
    leg.AddEntry(hists['sig'], '#bf{TChiWH(800,100)}', 'l')
    hists['sig2'].SetLineColor(1)
    hists['sig2'].SetLineWidth(2)
    hists['sig2'].SetLineStyle(2)
    leg.AddEntry(hists['sig2'], '#bf{TChiWH(425,150)}', 'l')
    hists['sig3'].SetLineColor(1)
    hists['sig3'].SetLineWidth(2)
    hists['sig3'].SetLineStyle(3)
    leg.AddEntry(hists['sig3'], '#bf{TChiWH(225,75)}', 'l')
    hists['data'].SetLineColor(1)
    hists['data'].SetLineWidth(1)
    hists['data'].SetMarkerStyle(8)
    leg.AddEntry(hists['data'], '#bf{Observed}', 'e1p')
    boxes[0].SetLineWidth(0)
    leg.AddEntry(boxes[0], '#bf{Uncertainty}', 'f')
    return [leg]

def drawObjects( isData=False, lumi=137 ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.05)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.945, 'CMS Simulation') if not isData else ( (0.15, 0.945, 'CMS') if not options.preliminary else (0.15, 0.945, 'CMS #bf{#it{Preliminary}}')),
      (0.70, 0.945, '#bf{%s fb^{-1} (13 TeV)}'%lumi )
    ]
    return [tex.DrawLatex(*l) for l in lines]

drawObjects = drawObjects(isData) + boxes + drawDivisions(regions) + drawTexLabels(regions) + getLegend()

plots = [ [hists['top'], hists['wjets'], hists['other']], [hists['data']], [hists['sig']], [hists['sig2']], [hists['sig3']] ]
#plots = [ [hists['top'], hists['wjets'], hists['other']], [hists['data']], [hists['sig']] ]

for log, l in [(False,'lin'),(True,'log')]:

    postFix = ''
    if options.postFit:
        postFix += '_postFit'

    postFix += '_%s'%l
    
    plotting.draw(
        Plot.fromHisto('signalRegions'+postFix,
                    plots,
                    texX = "E_{T}^{miss} (GeV)",
                    texY = 'Number of events',
                ),
        plot_directory = os.path.join('/home/users/dspitzba/public_html/WH_studies/', "signalRegions_unblind_test"),
        logX = False, logY = log, sorting = False, 
        legend = None,
        widths = {'x_width':800, 'y_width':600, 'y_ratio_width':250},
        yRange = (ymin,3000) if log else (0,30),
        drawObjects = drawObjects,
        ratio = {'yRange': (0.11, 2.19), 'texY':'Data/Pred.', 'histos':[(1,0)], 'histModifications': [lambda h: setBinLabels(h)], 'drawObjects':drawDivisionsRatio(regions)+ratio_boxes},
        copyIndexPHP = True,
    )

import pandas as pd

df = pd.DataFrame(dict_for_table)

#print df.to_latex(columns=['nJet','nHiggs', 'MET','top','wjets','other','total_background', 'sig', 'sig2', 'sig3'], index=False, escape=False)
print df.to_latex(columns=['nJet','nHiggs', 'MET','top','wjets','other','total_background', 'sig'], index=False, escape=False)
