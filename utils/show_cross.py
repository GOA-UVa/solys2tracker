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
        ax[0].scatter(x, ms[:mid])
        ax[0].grid()
        ax[1].set_title(f'Detector {i+1}: Zenit')
        ax[1].scatter(x, ms[mid:])
        ax[1].grid()
    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
