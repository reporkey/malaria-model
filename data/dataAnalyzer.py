import json
import os
import matplotlib.pyplot as plt
import numpy as np
from itertools import zip_longest


def normalizeRaw(raw):
	data = {}
	data['parameter'] = raw[0]['parameter']
	print(data['parameter'])
	data['time'] = max([each['time'] for each in raw])
	for component in raw[0].keys():
		if component == 'parameter' or component == 'time': continue
		data[component] = []
		l =  [raw[n][component][-300:] for n in range(len(raw))]
		r = [list(filter(None,i)) for i in zip_longest(*l)]
		data[component] = r
	return data

def plot():
	cases = [None,8,(30, 8),[16, 24, 30], [0, -1],slice(100, 200, 3),0.1, 0.3, 1.5,(0.0, 0.1), (0.45, 0.1)]
	figsize = (10, 8)
	cols = 3
	rows = len(cases) // cols + 1
	delta = 0.11
	x = np.linspace(0, 10 - 2 * delta, 200) + delta
	y = np.sin(x) + 1.0 + delta

	fig1, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
	axs = axs.flat
	for ax in axs[len(cases):]:
		ax.remove()
	axs = axs[:len(cases)]
	for ax, case in zip(axs, cases):
		ax.set_title('markevery=%s' % str(case))
		ax.plot(x, y, 'o', ls='-', ms=4, markevery=case)
		ax.fill_between(x, y, facecolor='blue', alpha=0.5)
	plt.show()


if __name__ == '__main__':
	#fs = os.listdir('./data/raw')
	#for fname in fs:
	#	with open('./data/raw/'+ fname, 'r') as f:
	#		raw = json.load(f)
	#	data = normalizeRaw(raw)
	#	with open('./data/preprocessed/' + fname, 'w') as f:
	#		json.dump(data, f)

	with open('./data/preprocessed/data1.json', 'r') as f:
		raw = json.load(f)
	plot()