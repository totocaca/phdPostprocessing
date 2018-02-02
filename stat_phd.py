#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 18:59:47 2017

@author: florian
"""

import os
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import collections
import matplotlib.cm as cm
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
import traces
import seaborn as sns
from bokeh.models import LinearAxis, Range1d, ContinuousAxis
from bokeh.models import ColumnDataSource, Whisker
from bokeh.layouts import gridplot
from bokeh.io import output_file, show, export_png, export_png
from bokeh.layouts import gridplot, layout
from bokeh.palettes import Viridis3
from bokeh.plotting import figure
import numpy as np
# import holoviews as hv
import matplotlib.gridspec as gridspec
import vapeplot
# vapeplot.set_palette('sunset')
pal =  sns.blend_palette(vapeplot.palette('vaporwave'))
# hv.extension('bokeh')

localData = np.load("localdata.npy")
globalData = np.load("globaldata.npy")
print globalData.shape, 'before'

g = 0
for i in xrange(globalData[:, 1].shape[0]):
    # print globalData[138-i,-1]
    if globalData[138 - i, -1] != 'nan':
        g = globalData[138 - i, -1]

    else:
        globalData[138 - i, -1] = g

# compute sorting index
ind = np.lexsort((globalData[:, 2].astype(float), globalData[:, -1].astype(float)))
indLoc = np.ones(localData.shape[0]) * np.nan
index = np.indices([600])
for i in xrange(globalData.shape[0]):
    indLoc[(i) * 600: (i + 1) * 600] = (ind[i] * 600) + index

globalData = globalData[ind]
indLoc = indLoc.astype(int)
localData = localData[indLoc]
print 'cm³'
globalVarNames = ['lastScan', 'patientId', 'scanId', 'ptName', 'AAA', 'Age (years)', 'Sexe (-)', 'IMC (-)', \
                  'Systolic pressure (mmHg)', 'Diastolic pressure (mmHg)', 'HTA (%)', 'nRxantiHTA (%)', 'DLP (%)', 'STATINES (%)', 'Lumen volume (cm³)', 'Thrombus volume (cm³)', \
                  'Total volume (cm³)', 'Total volume, annual (cm³/year)', 'vTot_monthly_2percentthreshold', 'Lumen surface area (cm²)', \
                  'Lumen shape factor (-)', 'Lumen Dmax (mm)', 'd0Lum', 'davgLum', 'Thrombus Dmax (mm)', 'dmaxTH_50mmthreshold', \
                  'd0TH', 'davgTH', 'Lumen volume, annual (cm³/year)', 'Lumen surface area, annual (cm²/year)', 'Lumen shape factor, annual (year⁻¹)' \
    , 'Lumen Dmax, annual (mm/year)', 'Thrombus Dmax, annual (mm/year)', 'dmaxTH_monthly5mmthreshold', \
                  'Thrombus volume, annual (cm³/year)', 'Lumen centerline tortuosity (-)', 'Lumen centerline tortuosity,annual (year⁻¹)', 'Lumen centerline curvature (m⁻²)', \
                  'Lumen centerline curvature, annual (m⁻²/year)', 'Divergence_average_max', 'WSSG max (Pa/m)', \
                  'OSI max (-)', 'PatchArea_max', 'RRT max (Pa⁻¹)', 'TAWSS max (Pa)', 'Thrombus thickness max (mm)', \
                  'ECAP max (Pa⁻¹)', 'Divergence_average_min', 'WSSG min (Pa/m)', \
                  'OSI min (-)', 'PatchArea_min', 'RRT min (Pa⁻¹)', 'TAWSS min (Pa)', 'Thrombus thickness min (mm)', \
                  'ECAP min (Pa⁻¹)', 'Divergence_average_mean', 'WSSG mean (Pa/m)', \
                  'OSI mean (-)', 'PatchArea_mean', 'RRT mean (Pa⁻¹)', 'TAWSS mean (Pa)', 'Thrombus thickness mean', \
                  'ECAP mean (Pa⁻¹)', 'Divergence_average_std', 'WSSG stdev (Pa/m)', 'OSI stdev (-)', \
                  'PatchArea_std', 'RRT stdev (Pa⁻¹)', 'TAWSS stdev (Pa)', 'Thrombus thickness stdev (mm)', 'ECAP stdev (Pa⁻¹)', \
                  'local lumen patch area mean, annual (mm²/year)', 'local lumen patch area max, annual (mm²/year)', \
                  'local lumen patch area min, annual (mm²/year)', 'local thrombus thickness mean, annual (mm²/year)', 'local thrombus thickness max, annual (mm²/year)', 'local thrombus thickness min, annual (mm²/year)', \
                  ' localDivAvgVarMean', 'localDivAvgVarMax', 'localDivAvgVarMin', 'local WSSG mean, annual (mm²/year)', \
                  'local WSSG max, annual (mm²/year)', 'local WSSG min, annual (mm²/year)', ' local OSI mean, annual (mm²/year)', 'local WSSG max, annual (mm²/year)', \
                  'local WSSG min, annual (mm²/year)', 'local RRT mean, annual (mm²/year)', 'local RRT max, annual (mm²/year)', 'local RRT min, annual (mm²/year)', \
                  'local TAWSS mean, annual (mm²/year)', ' local TAWSS max, annual (mm²/year)', 'local TAWSS min, annual (mm²/year)', 'local ECAP mean, annual (mm²/year)', \
                  'local ECAP max, annual (mm²/year)', 'local ECAP min, annual (mm²/year)', 'Thrombus coverage (%)', \
                  'Thrombus coverage, annual (%/year)', 'dt', 'CummulativeRisk', 'dMaxGrowthRegression', 'Time']

print len(globalVarNames)

localVarNames = ['AbscissaMetric', 'AngularMetric', 'BoundaryMetric', 'ClippingArray', \
                 'DistanceToCenterlines', 'Divergence_average', 'Gradients_average', \
                 'GroupIds', 'HarmonicMapping', 'OSI', 'PatchArea', 'RRT', 'Sector', \
                 'Slab', 'StretchedMapping', 'TAWSS', 'th_thickness', 'localLumAreaVar', \
                 'localThThVar', 'localDivAvgVar', 'localGradAvgVar', 'localOSIVar', \
                 'localRRTVar', 'localTAWSSVar', 'localECAPVar', 'ECAP', 'localDistToCtrl', \
                 'localDistToCtrlVar', 'thrombusGrowthThresh', 'stretchGrowthThresh', 'disToCtrlGrowthThresh']

AAAvsnoAAA = 0
riskvsnorisk = 1

idDmaxth = globalVarNames.index('dmaxTH_50mmthreshold')
idVolmax = globalVarNames.index('vTot_monthly_2percentthreshold')
CummulativeRisk = globalVarNames.index('CummulativeRisk')

localDataAAA = localData[:-5400, :]
localDatanoAAA = localData[-5399:, :]

globalDataAAA = globalData[:-10, :]
globalDatanoAAA = globalData[-9:, :]

globalDataAAARisky = globalDataAAA[globalDataAAA[:, CummulativeRisk] == 'True']
# globalDataAAARisky = globalDataAAARisky[globalDataAAARisky[:,idVolmax]=='True']
scanIdrisky = globalDataAAARisky[:, 2]
globalDataAAAnotRisky = globalDataAAA
nrowremoved = 0
for i in xrange(globalDataAAA.shape[0]):
    if globalDataAAA[i, 2] in scanIdrisky:
        #        print 'risk', i, i-nrowremoved
        globalDataAAAnotRisky = np.delete(globalDataAAAnotRisky, i - nrowremoved, 0)
        nrowremoved += 1

if AAAvsnoAAA:
    for i in xrange(globalData.shape[1]):
        if i not in [0, 3, 4, 18, 33, 6, 98, 25]:
            aaa = globalDataAAA[:, i].astype(float)
            noaaa = globalDatanoAAA[:, i].astype(float)
            #        print pdcolumnlist[i]
            #        print 'variance =', np.var(aaa), np.var(noaaa)
            #        print 'mean =', np.mean(aaa), np.mean(noaaa)
            #        print 'stdev =', np.std(aaa), np.std(noaaa)
            s, p = stats.ttest_ind(aaa, noaaa, equal_var=False, nan_policy='omit')
            if p < 0.001:
                p = '<0.001'
            # print globalVarNames[i],',',np.nanmean(aaa),',',np.nanstd(aaa), ',',np.nanmean(noaaa),',',np.nanstd(noaaa),',',p
    print '\n\n'

    for i in xrange(localData.shape[1]):
        if i not in [28, 29, 30]:
            aaa = localDataAAA[:, i].astype(float)
            noaaa = localDatanoAAA[:, i].astype(float)
            #        print pdcolumnlist[i]
            #        print 'variance =', np.var(aaa), np.var(noaaa)
            #        print 'mean =', np.mean(aaa), np.mean(noaaa)
            #        print 'stdev =', np.std(aaa), np.std(noaaa)
            s, p = stats.ttest_ind(aaa, noaaa, equal_var=False, nan_policy='omit')
            if p < 0.001:
                p = '<0.001'
            # print localVarNames[i],',',np.nanmean(aaa),',',np.nanstd(aaa), ',',np.nanmean(noaaa),',',np.nanstd(noaaa),',',p

if riskvsnorisk:
    for i in xrange(globalData.shape[1]):
        if i not in [0, 3, 4, 18, 33, 6, 98, 25]:
            #            print i
            risk = globalDataAAARisky[:, i].astype(float)
            norisk = globalDataAAAnotRisky[:, i].astype(float)
            #        print pdcolumnlist[i]
            #        print 'variance =', np.var(aaa), np.var(noaaa)
            #        print 'mean =', np.mean(aaa), np.mean(noaaa)
            #        print 'stdev =', np.std(aaa), np.std(noaaa)
            s, p = stats.ttest_ind(risk, norisk, equal_var=False, nan_policy='omit')
            # if p < 0.001:
            #     p = '<0.001'
            # print globalVarNames[i],',',np.nanmean(risk),',',np.nanstd(risk), ',',np.nanmean(norisk),',',np.nanstd(norisk),',',p
    print '\n\n'

nscans = []
globalData[:, 1] = globalData[:, 1].astype(int)
prev = globalData[0, 1]
cunt = 0
for i in xrange(globalData.shape[0]):
    if globalData[i, 1] == prev:
        cunt += 1
    else:
        nscans.append(cunt)
        cunt += 1
    prev = globalData[i, 1]

dt = np.empty([139])
globalData = np.insert(globalData, 100, 0, axis=1)

# lastcolumn = time (0, t1, t2+t1 etc)
prev = 0
for i in xrange(globalData[:, -1].shape[0]):
    globalData[i, -1] = prev
    if globalData[i, -4] == 'nan':
        prev = 0
    else:
        prev = globalData[i, -4].astype(float) + prev

a = np.split(globalData, nscans, axis=0)

time_seriesSlow = traces.TimeSeries()
time_seriesFast = traces.TimeSeries()

varID = 52
varname = globalVarNames[varID]
minVar = np.nanmin(globalData[:, varID].astype(float)) - 0.1 * np.nanmin(globalData[:, varID].astype(float))
maxVar = np.nanmax(globalData[:, varID].astype(float)) + 0.1 * np.nanmax(globalData[:, varID].astype(float))

p1 = figure(x_range=(-1, np.max(globalData[:, -1].astype(float) + 1)), y_range=(minVar, maxVar))
p1.grid.grid_line_alpha = 0.3
p1.xaxis.axis_label = 'Follow-up time (month)'
p1.yaxis.axis_label = varname
p1.extra_y_ranges = {"foo": Range1d(start=0, end=1)}
p1.add_layout(LinearAxis(y_range_name="foo", axis_label='Normalized averaged data over all patients'), 'right')
# p1.add_layout(LinearAxis(y_range_name="toto"), 'above')

for i in xrange(np.max(globalData[:, 1].astype(int))):
    # b= np.append(a[i][:,0], np.indices([a[i][:,0].shape[0]]).T.reshape(a[i][:,0].shape[0]), axis=1)
    index = list(np.indices([a[i][:, 0].shape[0]])[0])
    df2 = pd.DataFrame(a[i][:, [varID, -3, -1]], index=index)
    if df2[1][0] == 'True':
        for k in xrange(a[i][:, -1].shape[0]):
            time_seriesFast[a[i][k, -1].astype(float)] = (a[i][k, varID].astype(float) - minVar) / (maxVar - minVar)
        color = '#ffb3b3'
        # print 'Grand'
    else:
        for k in xrange(a[i][:, -1].shape[0]):
            time_seriesSlow[a[i][k, -1].astype(float)] = (a[i][k, varID].astype(float) - minVar) / (maxVar - minVar)

        color = '#b3b3ff'
    if i > 0:
        p1.line(df2[2], df2[0], color=color, line_width=4)
        # print df2[0]

quickAvg = time_seriesFast.moving_average(1, window_size=30, pandas=True)
quickAvg = pd.DataFrame(quickAvg, columns=[varname])

slowAvg = time_seriesSlow.moving_average(1, window_size=30, pandas=True)
slowAvg = pd.DataFrame(slowAvg, columns=[varname])

p1.line(quickAvg.index, quickAvg[varname], color='#ff0000', line_width=4, y_range_name="foo")
p1.line(slowAvg.index, slowAvg[varname], color='#0000ff', line_width=4, y_range_name="foo")

p2 = figure()
p2.line(slowAvg.index, slowAvg[varname], color='#f142f4', line_width=4, y_range_name="foo")

#
# show(p1)
# show(p2)

# grid = gridplot([p1, p2], ncols=2, plot_width=250, plot_height=250)
# show(grid)

varID = 9
varname = localVarNames[varID]

# p2 = figure(title='test')

# # print indLoc, indLoc.shape, type(indLoc), list(indLoc[:])
# l = list(indLoc[:].astype(int))
#
# preums = 0
# nscans.append(139)
# index = list(np.indices([599])[0])
# data = []
#
pl = []
l = 0
ll = []
indices = list(np.indices([600])[0])
# fig=plt.figure()
# # ax=fig.add_subplot(1,1,1)
# #fig, axes = plt.subplots(6, 6)
# sns.set()
# ax = []


# for ic in range(2):
#     for il in range(2):
#         ax.append(fig.add_subplot(4,ic+1,il+1))

sns.set_style("ticks")
sns.set_context("paper")

figsize = (6, 6)
cols = 6
cases = [1, 2, 3]
gs = gridspec.GridSpec((np.max(globalData[:, 1].astype(int)) + 5) // cols + 1, cols)
fig1 = plt.figure(num=1, figsize=figsize)
ax = []
fig1.subplots_adjust(hspace=.5)
j = 0
# print globalData[:, -1]
# print globalData[:, -2]
# print globalData[:, -3]


rc = [(0, 0),
      (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
      (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
      (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
      (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
      (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
      (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5)]

for i in xrange(np.max(globalData[:, 1].astype(int))):
    index = list(np.indices([a[i][:, 0].shape[0]])[0])
    ll = [x + l for x in index]
    # print i, index, l, ll,globalData[ll[-1], -2],'\n'
    # print 'patient ', i
    patchList = np.empty([600, len(ll)])
    j = 0
    for k in ll:
        patchList[:, j] = localData[k * 600:(k + 1) * 600, varID].astype(float)
        j += 1
    df = pd.DataFrame(data=patchList, index=indices)

    row = (i // cols)
    col = i % cols
    if (row, col) == (0, 0):
        ax.append(fig1.add_subplot(gs[0,:3]))
        toto = sns.boxplot(data=df, width=0.5, showfliers=False, linewidth=0.2, palette=pal)

    else:
        ax.append(fig1.add_subplot(gs[rc[i]]))

        toto = sns.boxplot(data=df, width=0.5, showfliers=False, linewidth=0.2, palette=pal)
    toto.tick_params(labelbottom='off')
    toto.set(ylim=(0, 0.5))

    '''
    if (row,col) == (0,0):
        #     ax.append( fig1.add_subplot(gs[row, col]))
        # if col == 0:
        ax.append(fig1.add_subplot(gs[0, 0]))
        # gs[row, col].tick_params(labelbottom='off')
        # ax[-1].boxplot(patchList, showfliers=False)
        print 'isain',i
        toto = sns.boxplot(data=df, width=0.5,showfliers=False,linewidth=0.2,palette=pal)

    # row += 1
    # col -= 1
    if (row in [1,2,3,4,5,6,7]) and (i != 0):
        #     ax.append( fig1.add_subplot(gs[row, col]))
        # if col in [0,1,2,3,4,5,6]:
        ax.append(fig1.add_subplot(gs[row, col]))
        # ax[-1].boxplot(patchList, showfliers=False)
        print 'ifast',i
        toto = sns.boxplot(data=df, width=0.5,showfliers=False,linewidth=0.2,palette=pal)
'''
    l += len(index)


# ax.plot(pl[0])
# plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()

# print pl
# plot_opts = dict(show_legend=False, width=400)
# style = dict(color='cyl')
# layout =([boxwhisker])
# hv.renderer('bokeh').save(boxwhisker, 'test', fmt='png')
# export_png(boxwhisker, filename="plot.png")
# for i in nscans:
#     n = i - prev
#     id = list(np.indices([n])[0] + prev)
#     # print prev, i, id, n
#     npArr = np.empty([599, n])
#     for k in xrange(n):
#         print (id[0] + k) * 600, (id[0] + k + 1) * 600 - 1
#         npArr[:, k] = localData[(id[0] + k) * 600:(id[0] + k + 1) * 600 - 1, varID]
#         df3 = pd.DataFrame(npArr, index=index)
#         toto = sns.boxplot(data=df3,  width=0.5, showfliers=False, linewidth=0.2)
#
#     prev = i
