import sys
import os

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
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



def main():
    folder_path = sys.argv[-1]
    mss = []
    files = sorted(os.listdir(folder_path))
    for path in files:
        meas = read_asdmeans(os.path.join(folder_path, path))
        mss.append(meas)
    mss = np.array(mss).T
    for i, ms in enumerate(mss):
        fig, ax = plt.subplots()
        lms = int(np.sqrt(len(ms)))
        ms = ms.reshape(lms, lms)
        min_max = _MINMAX
        min_d = -min_max
        max_d = min_max
        step = (max_d - min_d)/(lms-1)
        x = np.arange(min_d, max_d+step/2, step)
        ax.set_title(f'Detector {i+1}')
        im = ax.imshow(ms, origin='lower', cmap='bone', interpolation="none")
        x = np.array([f'{xi:.1f}' for xi in x])
        ax.set_xticks(np.arange(x.shape[0]), minor=True)
        ax.set_yticks(np.arange(x.shape[0]), minor=True)
        x = np.array([xi for xi in x[::2]])
        ax.set_xticks(np.arange(x.shape[0])*2, x)
        ax.set_yticks(np.arange(x.shape[0])*2, x)
        ax.set_xlabel('Zenit')
        ax.set_ylabel('Azimut')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')
        fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
