import json
import os
from natsort import natsorted
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.ticker as ticker
from matplotlib import cm
import numpy as np
from itertools import zip_longest
import scipy.stats as st


def normalizeRaw(raw):
	data = {}
	data['parameter'] = json.loads(raw[0]['parameter'])
	data['time'] = max([each['time'] for each in raw])
	for component in raw[0].keys():
		if component == 'parameter' or component == 'time': continue
		data[component] = []
		l = [raw[n][component][-300:] for n in range(len(raw))]
		r = list(zip_longest(*l))
		data[component] = r
	return data

def baselinePlot(data):
	# cases
	for d in data:
		if d['parameter']['beta_M_H'] == 0.2 and d['parameter']['beta_H_M'] == 0.2:
			y = np.array(d['i'], dtype=np.float)
			ym = np.array([np.median(each) for each in y]) / d['parameter']['N']
			ci95 = np.transpose(np.array([st.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=st.sem(a)) for a in y]) / d['parameter']['N'])
			y_m = np.array(d['im'], dtype=np.float)
			ym_m = np.array([np.median(each) for each in y_m])
			ci95_m = np.transpose(np.array([st.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=st.sem(a)) for a in y_m]))
			x = np.arange(0, len(ym))
	
	print(len(x))
	plt.grid(True)
	plt.title("Example full plot when "+r'$\beta_{MH}$: 0.2; $\beta_{HM}$: 0.2')
	plt.plot(x, ym)
	plt.plot(x, ym_m)
	plt.legend(["Median: "+str(round(np.mean(ym)*100, 1))+"%", ])
	plt.fill_between(x, ci95[0], ci95[1], facecolor='royalblue', alpha=0.5)
	plt.fill_between(x, ci95_m[0], ci95_m[1], facecolor='royalblue', alpha=0.5)
	plt.xlabel('Time(day)')
	plt.ylabel('Infectious Population')
	plt.show()

def mosBaselinePlot(data):
	# cases
	yl, yh, ym, x = [], [], [], []
	for d in data:
		if d['parameter']['beta_M_H'] == 0.2 and d['parameter']['beta_H_M'] == 0.2:
			y = np.array(d['im'], dtype=np.float)
			ym = np.array([np.median(each) for each in y])
			ci95 = np.transpose(np.array([st.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=st.sem(a)) for a in y]))
			x = np.arange(0, len(ym))
	
	print(len(x))
	plt.grid(True)
	plt.title("Example full plot when "+r'$\beta_{MH}$: 0.2; $\beta_{HM}$: 0.2')
	plt.plot(x, ym)
	plt.legend(["Median: "+str(round(np.mean(ym)*100, 1))+"%", ])
	plt.fill_between(x, ci95[0], ci95[1], facecolor='royalblue', alpha=0.5)
	plt.xlabel('Time(day)')
	plt.ylabel('Infectious Population')
	plt.show()

def mVsI(data):
	# cases
	i, im = [], []
	for d in data:
		if d['parameter']['beta_M_H'] == 0.2 and d['parameter']['beta_H_M'] == 0.2:
			i = np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N']
			im = np.median(np.array(d['im'], dtype=np.float), axis=1)
			x = np.arange(0, len(i))

	plt.title("Infection of Mosquito Baseline: "+r'$\beta_{MH}$: 0.8; $\beta_{HM}$: 0.3')
	plt.plot(x, i)
	plt.plot(x, im)
	plt.legend([r'i', r'im'])
	plt.xlabel('im')
	plt.ylabel('i')
	plt.show()

def betaPlot(data):
	xyMH = []
	xyHM = []
	for d in data:
		if d['parameter']['beta_H_M'] == 0.2:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyMH.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.2:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyHM.append((d['parameter']['beta_H_M'], aveMedian))

	plt.title(r'Comparison of Inflence from $\beta_{MH}$ and $\beta_{HM}$ in Population Model')
	plt.grid(True)
	xyMH.sort()
	x1,y1 = zip(*xyMH)
	xyHM.sort()
	x2,y2 = zip(*xyHM)
	plt.plot(y1, x1, 'o-')
	plt.plot(y2, x2, 'o-')
	plt.legend([r'$\beta_{MH}$ when $\beta_{HM}=0.2$', r'$\beta_{HM}$ when $\beta_{MH}=0.2$'])
	plt.xlabel('Infectious Population')
	plt.ylabel(r'$\beta$ value')
	plt.show()

def betaHMPlot(data):
	xyMH1 = []
	xyMH2 = []
	xyMH4 = []
	xyMH6 = []
	xyMH8 = []
	for d in data:
		if d['parameter']['beta_M_H'] == 0.1:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyMH1.append((d['parameter']['beta_H_M'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.2:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyMH2.append((d['parameter']['beta_H_M'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.4:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyMH4.append((d['parameter']['beta_H_M'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.6:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyMH6.append((d['parameter']['beta_H_M'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.8:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyMH8.append((d['parameter']['beta_H_M'], aveMedian))

	plt.title(r'$\beta_{HM}$ in Population Model')
	plt.grid(True)
	xyMH1.sort()
	x5,y5 = zip(*xyMH1)
	xyMH2.sort()
	x1,y1 = zip(*xyMH2)
	xyMH4.sort()
	x2,y2 = zip(*xyMH4)
	xyMH6.sort()
	x3,y3 = zip(*xyMH6)
	xyMH8.sort()
	x4,y4 = zip(*xyMH8)
	plt.plot(x5, y5, 'o-')
	plt.plot(x1, y1, 'o-')
	plt.plot(x2, y2, 'o-')
	plt.plot(x3, y3, 'o-')
	plt.plot(x4, y4, 'o-')
	plt.legend([r'$\beta_{MH}=0.1$', r'$\beta_{MH}=0.2$', r'$\beta_{MH}=0.4$', r'$\beta_{MH}=0.6$', r'$\beta_{MH}=0.8$'])
	plt.xlabel(r'$\beta_{HM}$')
	plt.ylabel('Infectious Population')
	plt.show()

def betaMHPlot(data):
	xyHM1 = []
	xyHM2 = []
	xyHM4 = []
	xyHM6 = []
	xyHM8 = []
	for d in data:
		if d['parameter']['beta_H_M'] == 0.1:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyHM1.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_H_M'] == 0.2:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyHM2.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_H_M'] == 0.4:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyHM4.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_H_M'] == 0.6:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyHM6.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_H_M'] == 0.8:
			aveMedian = np.mean(np.median(np.array(d['i'], dtype=np.float), axis=1) / d['parameter']['N'])
			xyHM8.append((d['parameter']['beta_M_H'], aveMedian))

	plt.title(r'$\beta_{MH}$ in Population Model')
	plt.grid(True)
	xyHM1.sort()
	x5,y5 = zip(*xyHM1)
	xyHM2.sort()
	x1,y1 = zip(*xyHM2)
	xyHM4.sort()
	x2,y2 = zip(*xyHM4)
	xyHM6.sort()
	x3,y3 = zip(*xyHM6)
	xyHM8.sort()
	x4,y4 = zip(*xyHM8)
	plt.plot(x5, y5, 'o-')
	plt.plot(x1, y1, 'o-')
	plt.plot(x2, y2, 'o-')
	plt.plot(x3, y3, 'o-')
	plt.plot(x4, y4, 'o-')
	plt.legend([r'$\beta_{HM}=0.1$', r'$\beta_{HM}=0.2$', r'$\beta_{HM}=0.4$', r'$\beta_{HM}=0.6$', r'$\beta_{HM}=0.8$'])
	plt.xlabel(r'$\beta_{MH}$')
	plt.ylabel('Infectious Population')
	plt.show()

def mosBetaHMPlot(data):
	xyMH1 = []
	xyMH2 = []
	xyMH4 = []
	xyMH6 = []
	xyMH8 = []
	for d in data:
		if d['parameter']['beta_M_H'] == 0.1:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyMH1.append((d['parameter']['beta_H_M'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.2:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyMH2.append((d['parameter']['beta_H_M'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.4:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyMH4.append((d['parameter']['beta_H_M'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.6:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyMH6.append((d['parameter']['beta_H_M'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.8:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyMH8.append((d['parameter']['beta_H_M'], aveMedian))

	plt.title(r'$\beta_{HM}$ in Population Model')
	plt.grid(True)
	xyMH1.sort()
	x5,y5 = zip(*xyMH1)
	xyMH2.sort()
	x1,y1 = zip(*xyMH2)
	xyMH4.sort()
	x2,y2 = zip(*xyMH4)
	xyMH6.sort()
	x3,y3 = zip(*xyMH6)
	xyMH8.sort()
	x4,y4 = zip(*xyMH8)
	plt.plot(x5, y5, 'o-')
	plt.plot(x1, y1, 'o-')
	plt.plot(x2, y2, 'o-')
	plt.plot(x3, y3, 'o-')
	plt.plot(x4, y4, 'o-')
	plt.legend([r'$\beta_{MH}=0.1$', r'$\beta_{MH}=0.2$', r'$\beta_{MH}=0.4$', r'$\beta_{MH}=0.6$', r'$\beta_{MH}=0.8$'])
	plt.xlabel(r'$\beta_{HM}$')
	plt.ylabel('Infectious Mosquitoes')
	plt.show()

def mosBetaMHPlot(data):
	xyHM1 = []
	xyHM2 = []
	xyHM4 = []
	xyHM6 = []
	xyHM8 = []
	for d in data:
		if d['parameter']['beta_H_M'] == 0.1:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyHM1.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_H_M'] == 0.2:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyHM2.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_H_M'] == 0.4:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyHM4.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_H_M'] == 0.6:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyHM6.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_H_M'] == 0.8:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyHM8.append((d['parameter']['beta_M_H'], aveMedian))

	plt.title(r'$\beta_{MH}$ in Population Model')
	plt.grid(True)
	xyHM1.sort()
	x5,y5 = zip(*xyHM1)
	xyHM2.sort()
	x1,y1 = zip(*xyHM2)
	xyHM4.sort()
	x2,y2 = zip(*xyHM4)
	xyHM6.sort()
	x3,y3 = zip(*xyHM6)
	xyHM8.sort()
	x4,y4 = zip(*xyHM8)
	plt.plot(x5, y5, 'o-')
	plt.plot(x1, y1, 'o-')
	plt.plot(x2, y2, 'o-')
	plt.plot(x3, y3, 'o-')
	plt.plot(x4, y4, 'o-')
	plt.legend([r'$\beta_{HM}=0.1$', r'$\beta_{HM}=0.2$', r'$\beta_{HM}=0.4$', r'$\beta_{HM}=0.6$', r'$\beta_{HM}=0.8$'])
	plt.xlabel(r'$\beta_{MH}$')
	plt.ylabel('Infectious Mosquitoes')
	plt.show()


def mosquitoBetaPlot(data):
	xyMH = []
	xyHM = []
	for d in data:
		if d['parameter']['beta_H_M'] == 0.2:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyMH.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.2:
			aveMedian = np.mean(np.median(np.array(d['im'], dtype=np.float), axis=1))
			xyHM.append((d['parameter']['beta_H_M'], aveMedian))

	plt.title(r'Proportion of infected mosquitoes with different $\beta$ in Multi-scaled Model')
	plt.grid(True)
	xyMH.sort()
	x1,y1 = zip(*xyMH)
	xyHM.sort()
	x2,y2 = zip(*xyHM)
	plt.plot(x1, y1, 'o-')
	plt.plot(x2, y2, 'o-')
	plt.legend([r'$\beta_{MH}$ when $\beta_{HM}=0.2$', r'$\beta_{HM}$ when $\beta_{MH}=0.2$'])
	plt.xlabel(r'$\beta$')
	plt.ylabel('Infectious Mosquitoes')
	plt.show()

def beta3DPlot(data):
	xy = []
	for d in data:
		aveMedian = np.mean(np.array([np.median(np.array(each, dtype=np.float)) for each in d['i']]) / d['parameter']['N'])
		xy.append((d['parameter']['beta_M_H'], d['parameter']['beta_H_M'], aveMedian))

	xy.sort()
	x1,x2,y = zip(*xy)
	x1 = np.array(x1)
	x2 = np.array(x2)
	y = np.array(y)
	ax = plt.axes(projection='3d')
	ax.plot_trisurf (x1, x2, y)
	ax.set_title(r'Epidemic with different $\beta$')

	plt.xlabel(r'$\beta_{MH}$')
	plt.ylabel(r'$\beta_{HM}$')
	#plt.zlabel('Infectious Population')
	plt.show()

def mosquitoBeta3DPlot(data):
	xy = []
	for d in data:
		aveMedian = np.mean(np.array([np.median(np.array(each, dtype=np.float)) for each in d['im']]) / d['parameter']['N'])
		xy.append((d['parameter']['beta_M_H'], d['parameter']['beta_H_M'], aveMedian))

	xy.sort()
	x1,x2,y = zip(*xy)
	x1 = np.array(x1)
	x2 = np.array(x2)
	y = np.array(y)
	ax = plt.axes(projection='3d')
	ax.plot_trisurf (x1, x2, y)
	ax.set_title(r'Proportion of infected mosquitoes with different $\beta$')

	plt.xlabel(r'$\beta_{MH}$')
	plt.ylabel(r'$\beta_{HM}$')
	#plt.zlabel('Infectious Population')
	plt.show()

def gVsI(data_p, data_m):


	return

if __name__ == '__main__':
	data_p = []
	fnames_p = os.listdir('./data/p')
	fnames_p = natsorted(fnames_p)

	for fname_p in fnames_p:
		with open('./data/p/' + fname_p, 'r') as f:
			raw = json.load(f)
		data_p.append(normalizeRaw(raw))

	data_m = []
	fnames_m = os.listdir('./data/m')
	fnames_m = natsorted(fnames_m)

	for fname_m in fnames_m:
		with open('./data/m/' + fname_m, 'r') as f:
			raw = json.load(f)
		data_m.append(normalizeRaw(raw))

	data_temp = []
	fnames_m = os.listdir('./data/raw2')
	fnames_m = natsorted(fnames_m)

	for fname_m in fnames_m:
		with open('./data/raw2/' + fname_m, 'r') as f:
			raw = json.load(f)
		data_temp.append(normalizeRaw(raw))
	
	#betaPlot(data_p)
	#betaMHPlot(data_temp)
	#betaHMPlot(data_temp)
	mosBetaMHPlot(data_p)
	mosBetaHMPlot(data_p)
	#mosquitoBetaPlot(data_p)
	#baselinePlot(data_p)
	#mosBaselinePlot(data_p)
	#beta3DPlot(data)
	#mosquitoBeta3DPlot(data)
	#mVsI(data_temp)