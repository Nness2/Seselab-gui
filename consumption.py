import numpy as np
import matplotlib.pyplot as plt

class Consumption:
    def __init__ (self, path):
        self._row = []
        self._column = []
        self._column2 = []
        self.creat_curve(path)

    def creat_plot (self):
        plt.plot(self._row[::-1], self._column[::-1], "b")
        plt.plot(self._row[::-1], self._column2[::-1], "g")
        plt.xlabel('Cycle')
        plt.ylabel('Consumption')
        plt.show() # affiche la figure a l'ecran

    def creat_curve (self, path):
        itr = 0
        with open(path, "r") as f:
            for line in f.readlines():
                self._row.insert(0, itr)
                self._column.insert(0, int(line.strip().split('\t')[0]))
                self._column2.insert(0, int(line.strip().split('\t')[1]))
                itr += 1