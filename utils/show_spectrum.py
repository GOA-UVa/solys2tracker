#!/usr/bin/env python

import sys
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def read_asd(path) -> pd.DataFrame:
    df = pd.read_csv(path, sep='\t', skiprows=4, decimal=',', names=['wlen', 'irr'], header=None)
    return df


def main():
    filename = sys.argv[-1]
    df = read_asd(filename)
    df.plot.scatter('wlen', 'irr', 2, grid=True, title='Espectro de mier')
    plt.show()


if __name__ == "__main__":
    main()
