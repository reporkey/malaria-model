import json
import os
from natsort import natsorted
import matplotlib.pyplot as plt
import numpy as np
from itertools import zip_longest


def normalizeRaw(raw):
	data = {}
	data['parameter'] = json.loads(raw[0]['parameter'])
	data['time'] = max([each['time'] for each in raw])
	for component in raw[0].keys():
		if component == 'parameter' or component == 'time': continue
		data[component] = []
		l = [raw[n][component][-300:] for n in range(len(raw))]
		r = [list(filter(None,i)) for i in zip_longest(*l)]
		data[component] = r
	return data

def fullplot(data):
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
		cases[i]['yl'] = np.array([np.amin(each) for each in data[i]['i']]) / data[i]['parameter']['N'] * 100
		cases[i]['yh'] = np.array([np.amax(each) for each in data[i]['i']]) / data[i]['parameter']['N'] * 100
		cases[i]['ym'] = np.array([np.median(each) for each in data[i]['i']]) / data[i]['parameter']['N'] * 100
		cases[i]['x'] = np.arange(-len(cases[i]['yl'])+1, 0+1)

	for ax, case in zip(axs, cases):
		ax.set_title(r'$\beta_{MH}$: '+str(round(case['beta_H_M'], 1))+r' $\beta_{HM}$: '+str(round(case['beta_M_H'], 1)))
		ax.plot(case['x'], case['ym'])
		ax.legend(["ave median: "+str(round(np.mean(case['ym']), 1)), ])
		ax.fill_between(case['x'], case['yl'], case['yh'], facecolor='royalblue', alpha=0.5)
	plt.show()


def betaplot(data):
	xyMH = []
	xyHM = []
	for d in data:
		if d['parameter']['beta_H_M'] == 0.3:
			aveMedian = round(np.mean(np.array([np.median(each) for each in d['i']]) / d['parameter']['N'] * 100), 1)
			xyMH.append((d['parameter']['beta_M_H'], aveMedian))
		if d['parameter']['beta_M_H'] == 0.8:
			aveMedian = round(np.mean(np.array([np.median(each) for each in d['i']]) / d['parameter']['N'] * 100), 1)
			xyHM.append((d['parameter']['beta_H_M'], aveMedian))

	print(xyMH)

	# print(xyHM)
	plt.title(r'Epidemic with different $\beta$')
	xyMH.sort()
	x1,y1 = zip(*xyMH)
	xyHM.sort()
	x2,y2 = zip(*xyHM)
	plt.plot(x1, y1, 'o-')
	plt.plot(x2, y2, 'o-')
	plt.legend([r'$\beta_{MH}$ vary; $\beta_{HM}=0.3$', r'$\beta_{HM}$ vary; $\beta_{MH}=0.8$'])
	plt.xlabel(r'$\beta$')
	plt.ylabel('Infectious Population')


	plt.show()


if __name__ == '__main__':
	data = []
	fnames = os.listdir('./data/raw')
	fnames = natsorted(fnames)

	for fname in fnames:
		with open('./data/raw/' + fname, 'r') as f:
			raw = json.load(f)
		data.append(normalizeRaw(raw))
	#fullplot(data)
	betaplot(data)