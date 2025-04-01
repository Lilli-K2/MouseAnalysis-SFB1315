import pandas as pd
import numpy as np
import re
from functools import reduce
import math
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
from datetime import datetime

"""
    ALWAYS
    change 'base' to desired filename
    read correct csv file into 'df'
    und 'rename' adjust column names to those found in your csv
    choose the correct conversion factor for the dataset
"""


base = "OutputFile"

df = pd.read_csv("NameOfYourFile.csv", low_memory=False)

df1 = df.iloc[2: , :]
print(df1)

#change to correct column name
df1.rename(columns={"DLC_resnet50_LastMouse4PointDec11shuffle1_500000": "XValueNose", "DLC_resnet50_LastMouse4PointDec11shuffle1_500000.2": "AccuracyNose"}, inplace=True)
df1.rename(columns={"DLC_resnet50_LastMouse4PointDec11shuffle1_500000.1": "YValueNose"}, inplace=True)
df1.rename(columns={"DLC_resnet50_LastMouse4PointDec11shuffle1_500000.3": "XValueNeck", "DLC_resnet50_LastMouse4PointDec11shuffle1_500000.5": "AccuracyNeck"}, inplace=True)
df1.rename(columns={"DLC_resnet50_LastMouse4PointDec11shuffle1_500000.4": "YValueNeck"}, inplace=True)
df1.rename(columns={"DLC_resnet50_LastMouse4PointDec11shuffle1_500000.6": "XValueButt", "DLC_resnet50_LastMouse4PointDec11shuffle1_500000.8": "AccuracyButt"}, inplace=True)
df1.rename(columns={"DLC_resnet50_LastMouse4PointDec11shuffle1_500000.7": "YValueButt"}, inplace=True)
df1.rename(columns={"DLC_resnet50_LastMouse4PointDec11shuffle1_500000.9": "XValueTail", "DLC_resnet50_LastMouse4PointDec11shuffle1_500000.11": "AccuracyTail"}, inplace=True)
df1.rename(columns={"DLC_resnet50_LastMouse4PointDec11shuffle1_500000.10": "YValueTail"}, inplace=True)


#generate timestamp as filename of upcoming csv files and pngs
filename = datetime.now().strftime("%Y%m%d_%H%M%S")

def format_scientific(value):
    try:
        return '{:.10f}'.format(float(value)).rstrip('0').rstrip('.')
    except ValueError:
        return value
df1['AccuracyNose']= df1['AccuracyNose'].apply(format_scientific)
df1['AccuracyNeck']= df1['AccuracyNeck'].apply(format_scientific)
df1['AccuracyButt']= df1['AccuracyButt'].apply(format_scientific)
df1['AccuracyTail']= df1['AccuracyTail'].apply(format_scientific)

df1.to_csv(f"{filename}_{base}_convert.csv")
dfAccuracyNose = df1["AccuracyNose"]
dfXNose = df1["XValueNose"]
dfYNose = df1["YValueNose"]
dfAccuracyNeck = df1["AccuracyNeck"]
dfXNeck = df1["XValueNeck"]
dfYNeck = df1["YValueNeck"]
dfAccuracyButt = df1["AccuracyButt"]
dfXButt = df1["XValueButt"]
dfYButt = df1["YValueButt"]
dfAccuracyTail = df1["AccuracyTail"]
dfXTail = df1["XValueTail"]
dfYTail = df1["YValueTail"]

#set the accuracy value
dfBadAccuracyNose = df1.query('AccuracyNose <="0.90"')
dfBadAccuracyNeck = df1.query('AccuracyNeck <="0.90"')
dfBadAccuracyButt = df1.query('AccuracyButt <="0.90"')
dfBadAccuracyTail = df1.query('AccuracyTail <="0.90"')

# avg 30 frames = 1s
total_rows = len(df1)
bad_countNose = len(dfBadAccuracyNose)
bad_percentageNose = 100/total_rows*bad_countNose
good_countNose = total_rows - bad_countNose
bad_countNeck = len(dfBadAccuracyNeck)
bad_percentageNeck = 100/total_rows*bad_countNeck
good_countNeck = total_rows - bad_countNeck
bad_countButt = len(dfBadAccuracyButt)
bad_percentageButt = 100/total_rows*bad_countButt
good_countButt = total_rows - bad_countButt
bad_countTail = len(dfBadAccuracyTail)
bad_percentageTail = 100/total_rows*bad_countTail
good_countTail = total_rows - bad_countTail

TotalBad_count = sum([bad_countNose, bad_countNeck, bad_countButt, bad_countTail])
TotalGood_count = 4*total_rows - TotalBad_count

plt.figure(1)
labels = ['Good Accuracy', 'Bad Accuracy']
sizes = [good_countNose, bad_countNose]
colors = ['#66b3ff', '#ff6666']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title("Good vs Bad Accuracy Nose")
plt.savefig(f"{filename}_{base}_GoodBadAccuracyNose.png")

df1Nose = df1.drop(dfBadAccuracyNose.index)
dfBadAccuracyNose.to_csv(f"{filename}_{base}_BadAccuracyNose.csv")
df1Nose = df1Nose.reset_index()
df1Nose.to_csv(f"{filename}_{base}_GoodValuesNose.csv")
TotalEntriesNose = df1Nose[df1Nose.columns[0]].count()
nb_row = 30

Nose_df = df1Nose.rolling(nb_row).mean()[nb_row::nb_row]
Nose_df.shape #no one knows what it does but nothing works without it
Nose_df.to_csv(f"{filename}_{base}_AveragesNose.csv")
Nose_df_every30 = df1Nose.iloc[::30].copy()
Nose_df.to_csv(f"{filename}_{base}_test30entriesNose.csv")
Nose_df["scorer"] = Nose_df_every30["scorer"]
Nose_df = Nose_df.reset_index()

dfXvalueNose = Nose_df["XValueNose"].shift(1)
dfyvalueNose = Nose_df["YValueNose"].shift(1)
dfXdefaultNose = Nose_df["XValueNose"]
dfydefaultNose = Nose_df["YValueNose"]
distancesNose = np.sqrt((dfXdefaultNose-dfXvalueNose)**2+(dfydefaultNose-dfyvalueNose)**2)

### Conversion factors:
#distances = (distances/px_per_cm)

# Pylon/Basler 4096x2160
#distancesNose = (distancesNose/42)

# OBS/MKV 1280x720
#distancesNose = (distancesNose/13.2)

# OBS/MP4 1920x1080
distancesNose = (distancesNose/20)

distancesNose = distancesNose.reset_index()
distancesNose.columns.values[1] = "distance"
Nose_df_every30["scorer"]=pd.to_numeric(Nose_df_every30["scorer"],errors="coerce")
Nose_df_every30["score_difference"] = Nose_df_every30["scorer"].diff()
Nose_df_every30.to_csv(f"{filename}_{base}_addedscorerNose.csv")
Nose_df_every30=Nose_df_every30.drop(index=0).reset_index(drop=True)
distancesNose["DistanceFrames"]=Nose_df_every30["score_difference"].values
distancesNose["DistanceFrames"] = distancesNose["DistanceFrames"] / 30
distancesNose = distancesNose.drop(index=0).reset_index(drop=True)

distancesNose["distance"] = distancesNose["distance"] / distancesNose["DistanceFrames"]
distancesNose["DistanceFrames"] = distancesNose["DistanceFrames"] / distancesNose["DistanceFrames"]
distancesNose.to_csv(f"{filename}_{base}_DistanceNoseWithScorer.csv")

dfdistanceValueNose = distancesNose
dfdistanceValueNose["DistanceNose"] = distancesNose.iloc[:, 1]
Nosemean_df = distancesNose.iloc[:, 1].mean()
Nosestd_dev = distancesNose.iloc[:, 1].std()
Nosemean_rounded = Nosemean_df.round(3)
Nosestd_dev_rounded = Nosestd_dev.round(3)

dfdistanceValueNose.to_csv(f"{filename}_{base}_FinalDistanceNose.csv")
distancesNose.to_csv(f"{filename}_{base}_beforeIloc.csv")
FullDistanceNose = sum(distancesNose.iloc[0:, 1])
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.figure(2)
labels = ['Good Accuracy', 'Bad Accuracy']
sizes = [good_countNeck, bad_countNeck]
colors = ['#66b3ff', '#ff6666']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title("Good vs Bad Accuracy Neck")
plt.savefig(f"{filename}_{base}_GoodBadAccuracyNeck.png")

df1Neck = df1.drop(dfBadAccuracyNeck.index)
dfBadAccuracyNeck.to_csv(f"{filename}_{base}_BadAccuracyNeck.csv")

df1Neck = df1Neck.reset_index()
df1Neck.to_csv(f"{filename}_{base}_GoodValuesNeck.csv")
TotalEntriesNeck = df1Neck[df1Neck.columns[0]].count()
nb_row = 30

Neck_df = df1Neck.rolling(nb_row).mean()[nb_row::nb_row]
Neck_df.shape
Neck_df.to_csv(f"{filename}_{base}_AveragesNeck.csv")
Neck_df_every30 = df1Neck.iloc[::30].copy()
Neck_df_every30.to_csv(f"{filename}_{base}_test30entriesNeck.csv")
Neck_df["scorer"] = Neck_df_every30["scorer"]
Neck_df = Neck_df.reset_index()

dfXvalueNeck = Neck_df["XValueNeck"].shift(1)
dfyvalueNeck = Neck_df["YValueNeck"].shift(1)
dfXdefaultNeck = Neck_df["XValueNeck"]
dfydefaultNeck = Neck_df["YValueNeck"]
distancesNeck = np.sqrt((dfXdefaultNeck-dfXvalueNeck)**2+(dfydefaultNeck-dfyvalueNeck)**2)

### Conversion factors:
#distances = (distances/px_per_cm)

# Pylon/Basler 4096x2160
#distancesNeck = (distancesNeck/42)

# OBS/MKV 1280x720
#distancesNeck = (distancesNeck/13.2)

# OBS/MP4 1920x1080
distancesNeck = (distancesNeck/20)

distancesNeck= distancesNeck.reset_index()
distancesNeck.columns.values[1] = "distance"
Neck_df_every30["scorer"]=pd.to_numeric(Neck_df_every30["scorer"],errors="coerce")
Neck_df_every30["score_difference"] = Neck_df_every30["scorer"].diff()
Neck_df_every30.to_csv(f"{filename}_{base}_addedscorerNeck.csv")
Neck_df_every30=Neck_df_every30.drop(index=0).reset_index(drop=True)
distancesNeck["DistanceFrames"]=Neck_df_every30["score_difference"].values
distancesNeck["DistanceFrames"] = distancesNeck["DistanceFrames"] / 30
distancesNeck = distancesNeck.drop(index=0).reset_index(drop=True)
distancesNeck["distance"] = distancesNeck["distance"] / distancesNeck["DistanceFrames"]
distancesNeck["DistanceFrames"] = distancesNeck["DistanceFrames"] / distancesNeck["DistanceFrames"]
distancesNeck.to_csv(f"{filename}_{base}_DistanceNeckWithScorer.csv")

dfdistanceValueNeck = distancesNeck
dfdistanceValueNeck["DistanceNeck"] = distancesNeck.iloc[:, 1]
Neckmean_df = distancesNeck.iloc[:, 1].mean()
Neckstd_dev = distancesNeck.iloc[:, 1].std()
Neckmean_rounded = Neckmean_df.round(3)
Neckstd_dev_rounded = Neckstd_dev.round(3)

dfdistanceValueNeck.to_csv(f"{filename}_{base}_FinalDistanceNeck.csv")
FullDistanceNeck = sum(distancesNeck.iloc[0:, 1])

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.figure(3)
labels = ['Good Accuracy', 'Bad Accuracy']
sizes = [good_countButt, bad_countButt]
colors = ['#66b3ff', '#ff6666']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title("Good vs Bad Accuracy Butt")
plt.savefig(f"{filename}_{base}_GoodBadAccuracyButt.png")

df1Butt = df1.drop(dfBadAccuracyButt.index)
dfBadAccuracyButt.to_csv(f"{filename}_{base}_BadAccuracyButt.csv")

df1Butt = df1Butt.reset_index()
df1Butt.to_csv(f"{filename}_{base}_GoodValuesButt.csv")
TotalEntriesButt = df1Butt[df1Butt.columns[0]].count()
nb_row = 30


Butt_df = df1Butt.rolling(nb_row).mean()[nb_row::nb_row]
Butt_df.shape #no one knows what it does but nothing works without it
Butt_df.to_csv(f"{filename}_{base}_AveragesButt.csv")
Butt_df_every30 = df1Butt.iloc[::30].copy()
Butt_df_every30.to_csv(f"{filename}_{base}_test30entriesButt.csv")
Butt_df["scorer"] = Butt_df_every30["scorer"]
Butt_df = Butt_df.reset_index()

dfXvalueButt = Butt_df["XValueButt"].shift(1)
dfyvalueButt = Butt_df["YValueButt"].shift(1)
dfXdefaultButt = Butt_df["XValueButt"]
dfydefaultButt = Butt_df["YValueButt"]
distancesButt = np.sqrt((dfXdefaultButt-dfXvalueButt)**2+(dfydefaultButt-dfyvalueButt)**2)

### Conversion factors:
#distances = (distances/px_per_cm)

# Pylon/Basler 4096x2160
#distancesButt = (distancesButt/42)

# OBS/MKV 1280x720
#distancesButt = (distancesButt/13.2)

# OBS/MP4 1920x1080
distancesButt = (distancesButt/20)

distancesButt = distancesButt.reset_index()
distancesButt.columns.values[1] = "distance"
Butt_df_every30["scorer"]=pd.to_numeric(Butt_df_every30["scorer"],errors="coerce")
Butt_df_every30["score_difference"] = Butt_df_every30["scorer"].diff()
Butt_df_every30.to_csv(f"{filename}_{base}_addedscorerButt.csv")
Butt_df_every30=Butt_df_every30.drop(index=0).reset_index(drop=True)
distancesButt["DistanceFrames"]=Butt_df_every30["score_difference"].values
distancesButt["DistanceFrames"] = distancesButt["DistanceFrames"] / 30
distancesButt = distancesButt.drop(index=0).reset_index(drop=True)

distancesButt["distance"] = distancesButt["distance"] / distancesButt["DistanceFrames"]
distancesButt["DistanceFrames"] = distancesButt["DistanceFrames"] / distancesButt["DistanceFrames"]
distancesButt.to_csv(f"{filename}_{base}_DistanceButtWithScorer.csv")

dfdistanceValueButt = distancesButt
dfdistanceValueButt["DistanceButt"] = distancesButt.iloc[:, 1]
Buttmean_df = distancesButt.iloc[:, 1].mean()
Buttstd_dev = distancesButt.iloc[:, 1].std()
Buttmean_rounded = Buttmean_df.round(3)
Buttstd_dev_rounded = Buttstd_dev.round(3)

dfdistanceValueButt.to_csv(f"{filename}_{base}_FinalDistanceButt.csv")
FullDistanceButt = sum(distancesButt.iloc[0:, 1])

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.figure(4)
labels = ['Good Accuracy', 'Bad Accuracy']
sizes = [good_countTail, bad_countTail]
colors = ['#66b3ff', '#ff6666']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title("Good vs Bad Accuracy Tail")
plt.savefig(f"{filename}_{base}_GoodBadAccuracyTail.png")

df1Tail = df1.drop(dfBadAccuracyTail.index)
dfBadAccuracyTail.to_csv(f"{filename}_{base}_BadAccuracyTail.csv")
df1Tail = df1Tail.reset_index()
df1Tail.to_csv(f"{filename}_{base}_BadAccuracyTail.csv")
TotalEntriesTail = df1Tail[df1Tail.columns[0]].count()
nb_row = 30

Tail_df = df1Tail.rolling(nb_row).mean()[nb_row::nb_row]
Tail_df.shape #no one knows what it does but nothing works without it
Tail_df.to_csv(f"{filename}_{base}_AveragesTail.csv")
Tail_df_every30 = df1Tail.iloc[::30].copy()
Tail_df_every30.to_csv(f"{filename}_{base}_test30entriesTail.csv")
Tail_df["scorer"] = Tail_df_every30["scorer"]
Tail_df = Tail_df.reset_index()

dfXvalueTail = Tail_df["XValueTail"].shift(1)
dfyvalueTail = Tail_df["YValueTail"].shift(1)
dfXdefaultTail = Tail_df["XValueTail"]
dfydefaultTail = Tail_df["YValueTail"]
distancesTail = np.sqrt((dfXdefaultTail-dfXvalueTail)**2+(dfydefaultTail-dfyvalueTail)**2)

### Conversion factors:
#distances = (distances/px_per_cm)

# Pylon/Basler 4096x2160
#distancesTail = (distancesTail/42)

# OBS/MKV 1280x720
#distancesTail = (distancesTail/13.2)

# OBS/MP4 1920x1080
distancesTail = (distancesTail/20)

distancesTail = distancesTail.reset_index()
distancesTail.columns.values[1] = "distance"
Tail_df_every30["scorer"]=pd.to_numeric(Tail_df_every30["scorer"],errors="coerce")
Tail_df_every30["score_difference"] = Tail_df_every30["scorer"].diff()
Tail_df_every30.to_csv(f"{filename}_{base}_addedscorerTail.csv")
Tail_df_every30=Tail_df_every30.drop(index=0).reset_index(drop=True)
distancesTail["DistanceFrames"]=Tail_df_every30["score_difference"].values
distancesTail["DistanceFrames"] = distancesTail["DistanceFrames"] / 30
distancesTail = distancesTail.drop(index=0).reset_index(drop=True)

distancesTail["distance"] = distancesTail["distance"] / distancesTail["DistanceFrames"]
distancesTail["DistanceFrames"] = distancesTail["DistanceFrames"] / distancesTail["DistanceFrames"]
distancesTail.to_csv(f"{filename}_{base}_DistanceTailWithScorer.csv")

dfdistanceValueTail = distancesTail
dfdistanceValueTail["DistanceTail"] = distancesTail.iloc[:, 1]
Tailmean_df = distancesTail.iloc[:, 1].mean()
Tailstd_dev = distancesTail.iloc[:, 1].std()
Tailmean_rounded = Tailmean_df.round(3)
Tailstd_dev_rounded = Tailstd_dev.round(3)

dfdistanceValueTail.to_csv(f"{filename}_{base}_FinalDistanceTail.csv")
FullDistanceTail = sum(distancesTail.iloc[0:, 1])

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.figure(5)
labels = ['Good Accuracy', 'Bad Accuracy']
sizes = [TotalGood_count, TotalBad_count]
colors = ['#66b3ff', '#ff6666']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title("Good vs Bad Accuracy Total")
plt.savefig(f"{filename}_{base}_GoodBadAccuracyTotal.png")

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.figure(6)
x_Nose = list(dfdistanceValueNose['index'])
activityindexNose = list(dfdistanceValueNose['DistanceNose'])

plt.plot(x_Nose, activityindexNose, linestyle='-', label='Mouse speed [cm/s]')

ax = plt.gca()
ymin, ymax = ax.get_ylim()
extra_space = (ymax - ymin) * 0.1
ax.set_ylim(ymin, ymax + extra_space)

bbox_props = dict(facecolor="lightblue", alpha=0.3, edgecolor="black", boxstyle="round,pad=0.5")
text = (f"Full Distance: {FullDistanceNose:.2f}cm\n"
        f"Average Distance: {Nosemean_rounded:.2f}cm\n"
        f"Standard deviation: {Nosestd_dev_rounded:.2f}")

plt.text(0.05, 0.96, text,
         transform=ax.transAxes,
         fontsize=10,
         verticalalignment='top',
         horizontalalignment='left',
         bbox=bbox_props)

plt.legend()
plt.title('Mouse [Nose]')
plt.xlabel('time [s]')
plt.ylabel('Distance [cm]')
plt.savefig(f"{filename}_{base}_FinalNose.png", dpi=500)
#plt.savefig(f"{filename}_{base}_FinalNose.svg")

plt.figure(7)
x_Neck = list(dfdistanceValueNeck['index'])
activityindexNeck = list(dfdistanceValueNeck['DistanceNeck'])

plt.plot(x_Neck, activityindexNeck, linestyle='-', label='Mouse speed [cm/s]')

ax = plt.gca()
ymin, ymax = ax.get_ylim()
extra_space = (ymax - ymin) * 0.1
ax.set_ylim(ymin, ymax + extra_space)

bbox_props = dict(facecolor="lightblue", alpha=0.3, edgecolor="black", boxstyle="round,pad=0.5")
text = (f"Full Distance: {FullDistanceNeck:.2f}cm\n"
        f"Average Distance: {Neckmean_rounded:.2f}cm\n"
        f"Standard deviation: {Neckstd_dev_rounded:.2f}")

plt.text(0.05, 0.96, text,
         transform=ax.transAxes,
         fontsize=10,
         verticalalignment='top',
         horizontalalignment='left',
         bbox=bbox_props)

plt.legend()
plt.title('Mouse [Neck]')
plt.xlabel('time [s]')
plt.ylabel('Distance [cm]')
plt.savefig(f"{filename}_{base}_FinalNeck.png", dpi=500)

plt.figure(8)
x_Butt = list(dfdistanceValueButt['index'])
activityindexButt = list(dfdistanceValueButt['DistanceButt'])

plt.plot(x_Butt, activityindexButt, linestyle='-', label='Mouse speed [cm/s]')

ax = plt.gca()
ymin, ymax = ax.get_ylim()
extra_space = (ymax - ymin) * 0.1
ax.set_ylim(ymin, ymax + extra_space)

bbox_props = dict(facecolor="lightblue", alpha=0.3, edgecolor="black", boxstyle="round,pad=0.5")
text = (f"Full Distance: {FullDistanceButt:.2f}cm\n"
        f"Average Distance: {Buttmean_rounded:.2f}cm\n"
        f"Standard deviation: {Buttstd_dev_rounded:.2f}")

plt.text(0.05, 0.96, text,
         transform=ax.transAxes,
         fontsize=10,
         verticalalignment='top',
         horizontalalignment='left',
         bbox=bbox_props)

plt.legend()
plt.title('Mouse [Butt]')
plt.xlabel('time [s]')
plt.ylabel('Distance [cm]')
plt.savefig(f"{filename}_{base}_FinalButt.png", dpi=500)

plt.figure(9)
x_Tail = list(dfdistanceValueTail['index'])
activityindexTail = list(dfdistanceValueTail['DistanceTail'])

plt.plot(x_Tail, activityindexTail, linestyle='-', label='Mouse speed [cm/s]')

ax = plt.gca()
ymin, ymax = ax.get_ylim()
extra_space = (ymax - ymin) * 0.1
ax.set_ylim(ymin, ymax + extra_space)

bbox_props = dict(facecolor="lightblue", alpha=0.3, edgecolor="black", boxstyle="round,pad=0.5")
text = (f"Full Distance: {FullDistanceTail:.2f}cm\n"
        f"Average Distance: {Tailmean_rounded:.2f}cm\n"
        f"Standard deviation: {Tailstd_dev_rounded:.2f}")

plt.text(0.05, 0.96, text,
         transform=ax.transAxes,
         fontsize=10,
         verticalalignment='top',
         horizontalalignment='left',
         bbox=bbox_props)

plt.legend()
plt.title('Mouse [Tail]')
plt.xlabel('time [s]')
plt.ylabel('Distance [cm]')
plt.savefig(f"{filename}_{base}_FinalTail.png", dpi=500)

df1Nose["XValueNose"] = df1Nose["XValueNose"].astype(float)
df1Nose["YValueNose"] = df1Nose["YValueNose"].astype(float)

dfHeatNose = df1Nose.iloc[:, [2, 3]]
dfHeatNose.to_csv(f"{filename}_{base}_newtest1.csv")
dfHeatNose = pd.DataFrame(dfHeatNose)

bin_size = 10
x_bins = np.arange(dfHeatNose['XValueNose'].min(), dfHeatNose['XValueNose'].max() + bin_size, bin_size)
y_bins = np.arange(dfHeatNose['YValueNose'].min(), dfHeatNose['YValueNose'].max() + bin_size, bin_size)

heatmap, xedges, yedges = np.histogram2d(dfHeatNose['XValueNose'], dfHeatNose['YValueNose'], bins=[x_bins, y_bins])

plt.figure((10), figsize=(8, 6))
sns.heatmap(heatmap.T,
            cmap='viridis', cbar=False,
            square=True,
            )
plt.title('Heatmap Mouse [Nose]')
#plt.xlabel('x')
#plt.ylabel('y')
plt.axis('off')
plt.savefig(f"{filename}_{base}_HeatmapNose.png", dpi=500)

plt.figure((11), figsize=(8, 6))
mask = (heatmap.T == 0)
sns.heatmap(heatmap.T,
            cmap='viridis', cbar=False,
            square=True,
            mask=mask,
            alpha=0.7
            )
plt.title('Heatmap Mouse [Nose]')
#plt.xlabel('x')
#plt.ylabel('y')
plt.axis('off')
plt.gcf().patch.set_facecolor('none')
plt.gca().patch.set_facecolor('none')
plt.savefig(f"{filename}_{base}_NoMaskHeatmapNose.png", dpi=500, transparent=True)

df1Neck["XValueNeck"] = df1Neck["XValueNeck"].astype(float)
df1Neck["YValueNeck"] = df1Neck["YValueNeck"].astype(float)

dfHeatNeck = df1Neck.iloc[:, [5, 6]]
dfHeatNeck.to_csv(f"{filename}_{base}_newtestneck1.csv")
dfHeatNeck = pd.DataFrame(dfHeatNeck)

bin_size = 10
x_bins = np.arange(dfHeatNeck['XValueNeck'].min(), dfHeatNeck['XValueNeck'].max() + bin_size, bin_size)
y_bins = np.arange(dfHeatNeck['YValueNeck'].min(), dfHeatNeck['YValueNeck'].max() + bin_size, bin_size)

heatmap, xedges, yedges = np.histogram2d(dfHeatNeck['XValueNeck'], dfHeatNeck['YValueNeck'], bins=[x_bins, y_bins])

plt.figure((12), figsize=(8, 6))
sns.heatmap(heatmap.T,
            cmap='viridis', cbar=False,
            square=True,
            )
plt.title('Heatmap Mouse [Neck]')
#plt.xlabel('x')
#plt.ylabel('y')
plt.axis('off')
plt.savefig(f"{filename}_{base}_HeatmapNeck.png", dpi=500)

plt.figure((13), figsize=(8, 6))
mask = (heatmap.T == 0)
sns.heatmap(heatmap.T,
            cmap='viridis', cbar=False,
            square=True,
            mask=mask,
            alpha=0.7
            )
plt.title('Heatmap Mouse [Neck]')
#plt.xlabel('x')
#plt.ylabel('y')
plt.axis('off')
plt.gcf().patch.set_facecolor('none')
plt.gca().patch.set_facecolor('none')
plt.savefig(f"{filename}_{base}_NoMaskHeatmapNeck.png", dpi=500, transparent=True)

df1Butt["XValueButt"] = df1Butt["XValueButt"].astype(float)
df1Butt["YValueButt"] = df1Butt["YValueButt"].astype(float)

dfHeatButt = df1Butt.iloc[:, [8, 9]]
dfHeatButt.to_csv(f"{filename}_{base}_newtestbutt1.csv")
dfHeatButt = pd.DataFrame(dfHeatButt)

bin_size = 10
x_bins = np.arange(dfHeatButt['XValueButt'].min(), dfHeatButt['XValueButt'].max() + bin_size, bin_size)
y_bins = np.arange(dfHeatButt['YValueButt'].min(), dfHeatButt['YValueButt'].max() + bin_size, bin_size)

heatmap, xedges, yedges = np.histogram2d(dfHeatButt['XValueButt'], dfHeatButt['YValueButt'], bins=[x_bins, y_bins])

plt.figure((14), figsize=(8, 6))
sns.heatmap(heatmap.T,
            cmap='viridis', cbar=False,
            square=True,
            )
plt.title('Heatmap Mouse [Butt]')
#plt.xlabel('x')
#plt.ylabel('y')
plt.axis('off')
plt.savefig(f"{filename}_{base}_HeatmapButt.png", dpi=500)

plt.figure((15), figsize=(8, 6))
mask = (heatmap.T == 0)
sns.heatmap(heatmap.T,
            cmap='viridis', cbar=False,
            square=True,
            mask=mask,
            alpha=0.7
            )
plt.title('Heatmap Mouse [Butt]')
#plt.xlabel('x')
#plt.ylabel('y')
plt.axis('off')
plt.gcf().patch.set_facecolor('none')
plt.gca().patch.set_facecolor('none')
plt.savefig(f"{filename}_{base}_NoMaskHeatmapButt.png", dpi=500, transparent=True)

df1Tail["XValueTail"] = df1Tail["XValueTail"].astype(float)
df1Tail["YValueTail"] = df1Tail["YValueTail"].astype(float)

dfHeatTail = df1Tail.iloc[:, [11, 12]]
dfHeatTail.to_csv(f"{filename}_{base}_newtesttail1.csv")
dfHeatTail = pd.DataFrame(dfHeatTail)

bin_size = 10
x_bins = np.arange(dfHeatTail['XValueTail'].min(), dfHeatTail['XValueTail'].max() + bin_size, bin_size)
y_bins = np.arange(dfHeatTail['YValueTail'].min(), dfHeatTail['YValueTail'].max() + bin_size, bin_size)

heatmap, xedges, yedges = np.histogram2d(dfHeatTail['XValueTail'], dfHeatTail['YValueTail'], bins=[x_bins, y_bins])

plt.figure((16), figsize=(8, 6))
sns.heatmap(heatmap.T,
            cmap='viridis', cbar=False,
            square=True,
            )
plt.title('Heatmap Mouse [Tail]')
#plt.xlabel('x')
#plt.ylabel('y')
plt.axis('off')
plt.savefig(f"{filename}_{base}_HeatmapTail.png", dpi=500)

plt.figure((17), figsize=(8, 6))
mask = (heatmap.T == 0)
sns.heatmap(heatmap.T,
            cmap='viridis', cbar=False,
            square=True,
            mask=mask,
            alpha=0.7
            )
plt.title('Heatmap Mouse [Tail]')
#plt.xlabel('x')
#plt.ylabel('y')
plt.axis('off')

plt.gcf().patch.set_facecolor('none')
plt.gca().patch.set_facecolor('none')

plt.savefig(f"{filename}_{base}_NoMaskHeatmapTail.png", dpi=500, transparent=True)

plt.show()
