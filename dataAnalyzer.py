import json
import os
from natsort import natsorted
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.ticker as ticker
from matplotlib import cm
import numpy as np
from itertools import zip_longest


def normalizeRaw(raw):
	data = {}
	data['parameter'] = json.loads(raw[0]['parameter'])
	data['time'] = max([each['time'] for each in raw])
	for component in raw[0].keys():
		if component == 'parameter' or component == 'time': continue
		data[component] = []
		l = [raw[n][component][-100:] for n in range(len(raw))]
		r = list(zip_longest(*l))
		data[component] = r
	return data

def fullPlot(data):
	# cases
	cases = []
	for d in data:
		cases.append({"beta_M_H": d['parameter']['beta_M_H'],
					  "beta_H_M": d['parameter']['beta_H_M']})

	# layout
	figsize = (10, 12)
	cols = 3
	rows = len(cases) // cols + 1
	fig1, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
	axs = axs.flat
	for ax in axs[len(cases):]:
		ax.remove()
	axs = axs[:len(cases)]

	# x, yl, ,ym, yh
	for i in range(len(data)):
		#cases[i]['yl'] = np.array([np.amin(each) for each in data[i]['i']]) / data[i]['parameter']['N']
		#cases[i]['yh'] = np.array([np.amax(each) for each in data[i]['i']]) / data[i]['parameter']['N']
		#cases[i]['ym'] = np.array([np.median(each) for each in data[i]['i']]) / data[i]['parameter']['N']

		cases[i]['yl'] = np.array(np.nanmin(np.array(data[i]['i'], dtype=np.float), axis=1)) / data[i]['parameter']['N']
		cases[i]['yh'] = np.array(np.nanmax(np.array(data[i]['i'], dtype=np.float), axis=1)) / data[i]['parameter']['N']
		cases[i]['ym'] = np.array(np.median(np.array(data[i]['i'], dtype=np.float), axis=1)) / data[i]['parameter']['N']
		cases[i]['im'] = np.array(np.median(np.array(data[i]['im'], dtype=np.float), axis=1)) / data[i]['parameter']['N']
		cases[i]['x'] = np.arange(0, len(cases[i]['yl']))

	for ax, case in zip(axs, cases):
		#ax.set_title(r'$\beta_{MH}$: '+str(round(case['beta_H_M'], 1))+r' $\beta_{HM}$: '+str(round(case['beta_M_H'], 1)))
		#ax.plot(case['x'], case['ym'])
		#ax.legend(["Median: "+str(round(np.mean(case['ym']*100), 1))+"%", ])
		#ax.fill_between(case['x'], case['yl'], case['yh'], facecolor='royalblue', alpha=0.5)
		print(r'$\beta_{MH}$: '+str(case['beta_H_M'])+r' $\beta_{HM}$: '+ str(case['beta_M_H']) + "\t" + str(round(np.mean(case['ym']*100), 2)) + "\t" + str(round(np.mean(case['im']*100), 6)))

	plt.show()

def mosquitoFullPlot(data):
	# cases
	cases = []
	for d in data:
		cases.append({"beta_M_H": d['parameter']['beta_M_H'],
					  "beta_H_M": d['parameter']['beta_H_M']})

	# layout
	figsize = (10, 12)
	cols = 3
	rows = len(cases) // cols + 1
	fig1, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
	axs = axs.flat
	for ax in axs[len(cases):]:
		ax.remove()
	axs = axs[:len(cases)]

	# x, yl, ,ym, yh
	for i in range(len(data)):
		cases[i]['yl'] = np.array([np.amin(each) for each in data[i]['im']]) / data[i]['parameter']['N']
		cases[i]['yh'] = np.array([np.amax(each) for each in data[i]['im']]) / data[i]['parameter']['N']
		cases[i]['ym'] = np.array([np.median(each) for each in data[i]['im']]) / data[i]['parameter']['N']
		cases[i]['x'] = np.arange(0, len(cases[i]['yl']))

	for ax, case in zip(axs, cases):
		ax.set_title(r'$\beta_{MH}$: '+str(round(case['beta_H_M'], 1))+r' $\beta_{HM}$: '+str(round(case['beta_M_H'], 1)))
		ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
		ax.plot(case['x'], case['ym'])
		ax.legend(["Median: {:0=.3f}e-7".format(np.mean(case['ym'])/1e-7), ])
		ax.fill_between(case['x'], case['yl'], case['yh'], facecolor='royalblue', alpha=0.5)
	plt.show()

def baselinePlot(data):
	# cases
	yl, yh, ym, x = [], [], [], []
	for d in data:
		if d['parameter']['beta_M_H'] == 0.8 and d['parameter']['beta_H_M'] == 0.3:
			yl = np.array([np.amin(each) for each in d['i']]) / d['parameter']['N']
			yh = np.array([np.amax(each) for each in d['i']]) / d['parameter']['N']
			ym = np.array([np.median(each) for each in d['i']]) / d['parameter']['N']
			x = np.arange(0, len(yl))

	plt.title("Baseline: "+r'$\beta_{MH}$: 0.8; $\beta_{HM}$: 0.3')
	plt.plot(x, ym)
	plt.legend(["Median: "+str(round(np.mean(ym)*100, 1))+"%", ])
	plt.fill_between(x, yl, yh, facecolor='royalblue', alpha=0.5)
	plt.xlabel('Time(day)')
	plt.ylabel('Infectious Population')
	plt.show()

def mosquitoBaselinePlot(data):
	# cases
	yl, yh, ym, x = [], [], [], []
	for d in data:
		if d['parameter']['beta_M_H'] == 0.8 and d['parameter']['beta_H_M'] == 0.3:
			yl = np.array([np.amin(each) for each in d['im']]) / d['parameter']['N']
			yh = np.array([np.amax(each) for each in d['im']]) / d['parameter']['N']
			ym = np.array([np.median(each) for each in d['im']]) / d['parameter']['N']
			x = np.arange(0, len(yl))

	plt.title("Infection of Mosquito Baseline: "+r'$\beta_{MH}$: 0.8; $\beta_{HM}$: 0.3')
	plt.plot(x, ym)
	plt.legend(["Median: {:0=.3f}e-5".format(np.mean(ym)/1e-5), ])
	plt.fill_between(x, yl, yh, facecolor='royalblue', alpha=0.5)
	plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
	plt.xlabel('Time(day)')
	plt.ylabel('Infectious Population(%)')
	plt.show()

def betaPlot(data):
	xyMH = []
	xyHM = []
	for d in data:
		if d['parameter']['beta_H_M'] == 0.4:
			aveMedian = np.mean(np.array([np.nanmedian(np.array(each,dtype=np.float64)) for each in d['i']]) / d['parameter']['N'])
			xyMH.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.8:
			aveMedian = np.mean(np.array([np.nanmedian(np.array(each,dtype=np.float64)) for each in d['i']]) / d['parameter']['N'])
			xyHM.append((d['parameter']['beta_H_M'], aveMedian))

	plt.title(r'Different $\beta$ in Population Model')
	plt.grid(True)
	xyMH.sort()
	x1,y1 = zip(*xyMH)
	xyHM.sort()
	x2,y2 = zip(*xyHM)
	plt.plot(x1, y1, 'o-')
	plt.plot(x2, y2, 'o-')
	plt.legend([r'$\beta_{MH}$ vary; $\beta_{HM}=0.4$', r'$\beta_{HM}$ vary; $\beta_{MH}=0.8$'])
	plt.xlabel(r'$\beta$')
	plt.ylabel('Infectious Population')
	plt.show()


def mosquitoBetaPlot(data):
	xyMH = []
	xyHM = []
	for d in data:
		if d['parameter']['beta_H_M'] == 0.4:
			aveMedian = np.mean(np.array([np.median(each) for each in d['im']]) / d['parameter']['N'])
			xyMH.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.8:
			aveMedian = np.mean(np.array([np.median(each) for each in d['im']]) / d['parameter']['N'])
			xyHM.append((d['parameter']['beta_H_M'], aveMedian))

	plt.title(r'Proportion of infected mosquitoes with different $\beta$ in Population Model')
	plt.grid(True)
	xyMH.sort()
	x1,y1 = zip(*xyMH)
	xyHM.sort()
	x2,y2 = zip(*xyHM)
	plt.plot(x1, y1, 'o-')
	plt.plot(x2, y2, 'o-')
	plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
	plt.legend([r'$\beta_{MH}$ vary; $\beta_{HM}=0.4$', r'$\beta_{HM}$ vary; $\beta_{MH}=0.8$'])
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

if __name__ == '__main__':
	data = []
	fnames = os.listdir('./data/raw1')
	fnames = natsorted(fnames)

	for fname in fnames:
		with open('./data/raw1/' + fname, 'r') as f:
			raw = json.load(f)
		data.append(normalizeRaw(raw))
	#fullPlot(data)
	#mosquitoBaselinePlot(data)
	#betaPlot(data)
	mosquitoBetaPlot(data)
	#baselinePlot(data)
	#mosquitoFullPlot(data)
	#beta3DPlot(data)
	#mosquitoBeta3DPlot(data)