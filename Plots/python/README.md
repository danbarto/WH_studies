# Plotting

Some very basic examples of plot scripts, using different python frameworks.

`WH_FastFullSim.py` produces a selection of plots to compare FullSim and FastSim WH samples.
It uses the RootTools framework to create histograms and plot.

`HiggsTag_FullFast.py` is an example for using the plottery framework, which just creates nice plots (no histogramming).



```
combine --forceRecreateNLL -M FitDiagnostics --saveShapes --saveNormalizations --numToysForShape 500 --saveOverall --saveWithUncertainties datacard.txt
python diffNuisances.py  fitDiagnostics.root &> nuisances.txt
python diffNuisances.py -a fitDiagnostics.root &> nuisances_full.txt
```
