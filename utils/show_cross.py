#!/usr/bin/env python

import sys
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


_MINMAX = 0.8

def read_asdmeans(path):
    df = pd.read_csv(path, sep='\t', skiprows=4, decimal=',', names=['wlen', 'irr'], header=None)
    #m1 = df[df['wlen']<=1000]['irr'].mean()
    m1 = df[(df['wlen']>=545) & (df['wlen']<=555)]['irr'].mean()
    #m2 = df[(df['wlen']>1000)&(df['wlen']<1800)]['irr'].mean()
    m2 = df[(df['wlen']>=1635) & (df['wlen']<=1645)]['irr'].mean()
    #m3 = df[df['wlen']>=1800]['irr'].mean()
    m3 = df[(df['wlen']>=2195) & (df['wlen']<=2205)]['irr'].mean()
    return m1, m2, m3


def normalize_both(arr0, arr1, t_min=0, t_max=1, minarr=None):
    diff = t_max - t_min
    if minarr is None:
        minarr = min(min(arr0), min(arr1))
    maxarr = max(max(arr0), max(arr1))
    diff_arr = maxarr - minarr
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
    minarrs = [None, None, None]
    min_max = float(sys.argv[2]) if len(sys.argv) > 2 else _MINMAX
    do_norm = bool(sys.argv[3]) if len(sys.argv) > 3 else False
    minarrs[0] = float(sys.argv[4]) if len(sys.argv) > 4 else None
    minarrs[1] = float(sys.argv[5]) if len(sys.argv) > 5 else None
    minarrs[2] = float(sys.argv[6]) if len(sys.argv) > 6 else None
    min_d = -min_max
    max_d = min_max
    mss = []
    files = sorted(os.listdir(folder_path))
    for path in files:
        meas = read_asdmeans(os.path.join(folder_path, path))
        mss.append(meas)
    mss = np.array(mss).T
    fig = plt.figure()
    axis = fig.subplots(3, 2)
    for i, (ax, ms, minarr) in enumerate(zip(axis, mss, minarrs)):
        lms = len(ms)
        step = 2*(max_d - min_d)/(lms-2)
        x = np.arange(min_d, max_d+step/2, step)
        mid = int(lms/2)
        if do_norm:
            norm0, norm1 = normalize_both(ms[:mid], ms[mid:], minarr=minarr)
        else:
            norm0, norm1 = (ms[:mid], ms[mid:])
        ax[0].set_title(f'Detector {i+1}: Azimut')
        ax[0].scatter(x, norm0)
        ax[0].grid()
        ax[1].set_title(f'Detector {i+1}: Zenit')
        ax[1].scatter(x, norm1)
        ax[1].grid()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
