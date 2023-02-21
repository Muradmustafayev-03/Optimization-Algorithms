import numpy as np
from copy import deepcopy


class HarmonySearch:
    """
    Optimization using metaheuristic Harmony Search Algorithm,
    that finds the minimum of the function, improvising harmonies.

    Attributes
    ----------
    func : callable
        Function to minimize
    d: int
        Number of dimensions of the function [f(x) = f(x_1, ..., x_d)]
    _range: float
        Range of values for the initial population x_1 in (-range/2; range/2)

    Methods
    -------
    generate_hm(hms: int)
        Generates initial Harmony Memory of random harmonies.

    eval(self, hm: numpy.array)
        Evaluates the given Harmony Memory to the function.

    improvise(self, hm: np.array, hmcr: float, par: float, bw: float)
        Improvises a new Harmony Memory out of the given one.

    change_hm(self, old_hm: np.array, new_hm: np.array)
        Replaces the worst harmony of the Old Harmony Memory with a better one.

    find_harmony(self, hms=30, max_iterations=10000, hmcr=0.8, par=0.4, bw=2)
        Finds the global minima of the function.
    :return:
    """
    def __init__(self, f: callable, d: int, hms: int, hmcr: float, par: float, bw: float, max_iter: int = 10**5,
                 rand_min: float = 0, rand_max: float = 1):
        """
        Parameters
        ----------
        func : callable
            Function to minimize
        d: int
            Number of dimensions of the function [f(x) = f(x_1, ..., x_d)]
        _range: float
            Range of values for the initial population x_1 in (-range/2; range/2)

        :return: None
        """
        self.f = f
        self.d = d
        self.hms = hms
        self.hmcr = hmcr
        self.par = par
        self.bw = bw
        self.max_iter = max_iter
        self.rand_min = rand_min
        self.rand_max = rand_max

    def generate_hm(self):
        """
        Generates initial Harmony Memory of random harmonies.

        Parameters
        ----------
        hms: int
            Harmony Memory Size, number of harmonies in Harmony Memory

        Returns
        -------
        :return: numpy.array: Harmony Memory
        """
        return np.random.uniform(self.rand_min, self.rand_max, (self.hms, self.d))

    def eval(self, hm: np.array):
        """
        Evaluates the given Harmony Memory to the function.

        Parameters
        ----------
        hm: numpy.array
            Harmony Memory, array of harmonies

        Returns
        -------
        :return: numpy.array: fittness values of all the harmonies
        """
        return np.apply_along_axis(self.f, 1, hm)
    
    def improvise(self, hm: np.array):
        """
        Improvises a new Harmony Memory out of the given one.

        Parameters
        ----------
        hm: numpy.array
            Harmony Memory, array of harmonies
        hmcr: float
            Share of harmonies to replace with a random harmony
        par: float
            Share of notes in a harmony to shift
        bw: float
            Shift range for notes to change

        Returns
        -------
        :return: numpy.array: new improvised Harmony Memory
        """
        new_hm = deepcopy(hm)

        for row in range(len(hm)):
            new_hm[row][np.random.rand() > self.hmcr] = np.random.uniform(self.rand_min, self.rand_max, 1)
            new_hm[row][np.random.rand() > self.par] += np.random.uniform(-self.bw, self.bw, 1)

        return new_hm

    def change_hm(self, old_hm: np.array, new_hm: np.array):
        """
        Replaces the worst harmony of the Old Harmony Memory
        with the best one from the New Harmony Memory if it is better.

        Parameters
        ----------
        old_hm: numpy.array
            Old Harmony Memory
        new_hm:
            New Harmony Memory

        Returns
        -------
        :return: numpy.array: changed hm
        """
        old_results = self.eval(old_hm)
        new_results = self.eval(new_hm)

        old_worst_i = np.argmax(old_results)
        new_best_i = np.argmin(new_results)

        if float(new_results[new_best_i]) < float(old_results[old_worst_i]):
            old_hm[old_worst_i] = new_hm[new_best_i]

        return old_hm

    def find_harmony(self):
        """
        Finds the global minima of the function.

        Parameters
        ----------
        hms: int
            Harmony Memory Size, number of harmonies in Harmony Memory
        max_iterations: int
            Maximal number of iterations
        hmcr: float
            Share of harmonies to replace with a random harmony
        par: float
            Share of notes in a harmony to shift
        bw: float
            Shift range for notes to change

        Returns
        -------
        :return: numpy.array
            x_min = (x_1, ..., x_d) where f(x_min) = min f(x)
        """
        hm = self.generate_hm()
        results = self.eval(hm)

        for _ in range(self.max_iter):
            new_hm = self.improvise(hm)
            hm = self.change_hm(hm, new_hm)
            results = self.eval(hm)

        best_i = np.argmin(results)
        return hm[best_i]
