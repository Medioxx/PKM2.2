import numpy as np
import random


def cluster_points(X, mu):
    '''
    Opis: Przypisanie danych do klastrow
    Zmienne wejściowe: dane, centra klastrów
    Zmienne wyjsciowe: dane przypisane do klastrów
    '''
    clusters = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm(x - mu[i[0]])) \
                         for i in enumerate(mu)], key=lambda t: t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters


def reevaluate_centers(mu, clusters):
    '''
    Opis: Zmiana położenia centrów
    Zmienne wejściowe: centra klastrów, dane przypisane do klastrów
    Zmienne wyjsciowe: nowe centra klastrów
    '''
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis=0))
    return newmu


def has_converged(mu, oldmu):
    '''
    Opis: Sprawdza zbieżność
    Zmienne wejściowe: losowo wygenerowane centra, losowo wygenerowane centra
    Zmienne wyjsciowe: True w przypadku zbieznoci/False w przeciwnym wypadku
    '''
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))

def find_centers(X, K):
    '''
    Opis: Znajduje centra skupisk danych
    Zmienne wejściowe: dane do klasteryzacji, ilosc centrow
    Zmienne wyjsciowe: wspolrzedne centrow, dane pogrupowane zgodnie z przynaleznoscia do klastrow
    '''
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return (mu, clusters)