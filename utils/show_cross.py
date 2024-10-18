#!/usr/bin/env python

import sys
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


_MINMAX = 0.8

def read_asdmeans(path):
    df = pd.read_csv(path, sep='\t', skiprows=4, decimal=',', names=['wlen', 'irr'], header=None)
    m1 = df[df['wlen']<=1000]['irr'].mean()
    m2 = df[(df['wlen']>1000)&(df['wlen']<1800)]['irr'].mean()
    m3 = df[df['wlen']>=1800]['irr'].mean()
    return m1, m2, m3


def normalize_both(arr0, arr1, t_min=0, t_max=1):
    diff = t_max - t_min
    minarr = min(min(arr0), min(arr1))
    diff_arr = max(max(arr0), max(arr1)) - minarr
    narrs = []
    for arr in [arr0, arr1]:
        norm_arr = []
        for i in arr:
            temp = (((i - minarr)*diff)/diff_arr) + t_min
            norm_arr.append(temp)
        narrs.append(norm_arr)
    return narrs[0], narrs[1]


def main():
    folder_path = sys.argv[1]
    min_max = _MINMAX
    if len(sys.argv) > 2:
        min_max = float(sys.argv[2])
    min = -min_max
    max = min_max
    mss = []
    files = sorted(os.listdir(folder_path))
    for path in files:
        meas = read_asdmeans(os.path.join(folder_path, path))
        mss.append(meas)
    mss = np.array(mss).T
    fig = plt.figure()
    axis = fig.subplots(3, 2)
    for i, (ax, ms) in enumerate(zip(axis, mss)):
        lms = len(ms)
        step = 2*(max - min)/(lms-2)
        x = np.arange(min, max+step, step)
        mid = int(lms/2)
        ax[0].set_title(f'Detector {i+1}: Azimut')
        norm0, norm1 = normalize_both(ms[:mid], ms[mid:])
        ax[0].scatter(x, norm0)
        ax[0].grid()
        ax[1].set_title(f'Detector {i+1}: Zenit')
        ax[1].scatter(x, norm1)
        ax[1].grid()
    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
