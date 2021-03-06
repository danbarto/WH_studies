#!/usr/bin/env bash

function print_commands {
    dsname=$1
    nicename=$(echo $dsname | cut -d '/' -f2-3 | sed 's|\/|__|g')
    files=$(./dis_client.py -t files -d "$dsname | grep name")
    for f in $files ; do
        tailname=$(echo $f | rev | cut -d '/' -f1 | rev)
        echo xrdcp root://cmsxrootd.fnal.gov/$f root://redirector.t2.ucsd.edu//store/user/dspitzba/nanoAOD/$nicename/$tailname
    done
}

# ./print_download_commands.sh > commands.txt; ./parallel --nice 10 --jobs 10 --bar --joblog joblog.txt < commands.txt

#print_commands /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM
#print_commands /TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv4-PUSummer16v3Fast_Nano14Dec2018_lhe_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM
#print_commands /tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
#print_commands /ST_tWll_5f_LO_TuneCP5_PSweights_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
#print_commands /ST_tWnunu_5f_LO_TuneCP5_PSweights_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
#print_commands /ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
#print_commands /THQ_4f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
#print_commands /THW_5f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
#print_commands /ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
#print_commands /ST_t-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
#print_commands /TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext2-v1/NANOAODSIM
#print_commands /TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext2-v1/NANOAODSIM
#print_commands /TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
#print_commands /TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
#print_commands /WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
#print_commands /WWTo2L2Nu_DoubleScattering_13TeV-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
print_commands /WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
print_commands /ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
print_commands /ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
print_commands /WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
print_commands /WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
print_commands /WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/NANOAODSIM
print_commands /WZTo3LNu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
print_commands /WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
print_commands /WWZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
print_commands /WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
print_commands /ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
