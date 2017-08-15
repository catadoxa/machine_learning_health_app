from sklearn.cluster import KMeans
from pprint import pprint
from .data import Data
import numpy as np
import random
#import matplotlib.pyplot as plt

class KMeansClusteringAnalysis():

    def __init__(self, data):
        self.matrix = self.extract_data_to_array(data)
        self.kmeans = KMeans(2)
        self.kmeans.fit(self.matrix)
        self.centers = self.calc_centers(data)
        self.return_data = self.create_return_data(data)

    def create_return_data(self, data):
        cluster_data = []
        for center in self.centers:
            center_data = {}
            for i in range(len(data.names)):
                center_data[data.names[i]] = "{0:.2f}".format(center[i])
            cluster_data.append(center_data)
        return cluster_data

    def calc_centers(self, data):
        centers = []
        for center in self.kmeans.cluster_centers_:
            centers.append(np.subtract(center, data.averages))
        return centers

    def extract_data_to_array(self, data):
        X = [value for value in data.data_dict.values()]
        return np.array(X)

    def calc_n(self):
        ks, logWks, logWkbs, sk = self.gap_statistic(self.matrix)
        gapK = []
        calc = []
        for i in range(len(ks)):
            gapK.append(logWkbs[i] - logWks[i])
        for i in range(len(ks) - 1):
            calc.append(gapK[i] - gapK[i+1] + sk[i+1])
        for val in calc:
            if val > 0:
                n = calc.index(val)
                break
        if n < 2:
            n = 2
        kmeans = KMeans(n)
        kmeans.fit(self.matrix)
        return kmeans

    # borrowed code from https://datasciencelab.wordpress.com/2013/12/12/clustering-with-k-means-in-python/
    # and https://datasciencelab.wordpress.com/2013/12/27/finding-the-k-in-k-means-clustering/
    def cluster_points(self, X, mu):
        clusters = {}
        for x in X:
            bestmukey = min([(i[0], np.linalg.norm(x - mu[i[0]])) \
                             for i in enumerate(mu)], key=lambda t: t[1])[0]
            try:
                clusters[bestmukey].append(x)
            except KeyError:
                clusters[bestmukey] = [x]
        return clusters

    def reevaluate_centers(self, mu, clusters):
        newmu = []
        keys = sorted(clusters.keys())
        for k in keys:
            newmu.append(np.mean(clusters[k], axis=0))
        return newmu

    def has_converged(self, mu, oldmu):
        return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))

    def find_centers(self, X, K):
        # Initialize to K random centers
        oldmu = random.sample(list(X), K)
        mu = random.sample(list(X), K)
        while not self.has_converged(mu, oldmu):
            oldmu = mu
            # Assign all points in X to clusters
            clusters = self.cluster_points(X, mu)
            # Reevaluate centers
            mu = self.reevaluate_centers(oldmu, clusters)
        return (mu, clusters)

    def Wk(self, mu, clusters):
        K = len(mu)
        return sum([np.linalg.norm(mu[i] - c) ** 2 / (2 * len(c)) for i in range(K) for c in clusters[i]])

    def bounding_box(self, X):
        xmin, xmax = min(X, key=lambda a: a[0])[0], max(X, key=lambda a: a[0])[0]
        ymin, ymax = min(X, key=lambda a: a[1])[1], max(X, key=lambda a: a[1])[1]
        return (xmin, xmax), (ymin, ymax)

    def gap_statistic(self, X):
        (xmin, xmax), (ymin, ymax) = self.bounding_box(X)
        # Dispersion for real distribution
        ks = range(1, 10)
        Wks = np.zeros(len(ks))
        Wkbs = np.zeros(len(ks))
        sk = np.zeros(len(ks))
        for indk, k in enumerate(ks):
            mu, clusters = self.find_centers(X, k)
            Wks[indk] = np.log(self.Wk(mu, clusters))
            # Create B reference datasets
            B = 10
            BWkbs = np.zeros(B)
            for i in range(B):
                Xb = []
                for n in range(len(X)):
                    Xb.append([random.uniform(xmin, xmax),
                               random.uniform(ymin, ymax)])
                Xb = np.array(Xb)
                mu, clusters = self.find_centers(Xb, k)
                BWkbs[i] = np.log(self.Wk(mu, clusters))
            Wkbs[indk] = sum(BWkbs) / B
            sk[indk] = np.sqrt(sum((BWkbs - Wkbs[indk]) ** 2) / B)
        sk = sk * np.sqrt(1 + 1 / B)
        return (ks, Wks, Wkbs, sk)


def init_board_gauss(N, k):
    n = float(N)/k
    X = []
    for i in range(k):
        c = (random.uniform(-1, 1), random.uniform(-1, 1))
        s = random.uniform(0.05,0.5)
        x = []
        while len(x) < n:
            a, b = np.array([np.random.normal(c[0], s), np.random.normal(c[1], s)])
            # Continue drawing points from the distribution in the range [-1,1]
            if abs(a) < 1 and abs(b) < 1:
                x.append([a,b])
        X.extend(x)
    X = np.array(X)[:N]
    return X

