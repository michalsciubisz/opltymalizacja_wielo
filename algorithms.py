import numpy as np
import time
import matplotlib.pyplot as plt

def algorytm_bez_filtracji(X):
    start_time = time.time()
    X_list = X.tolist()
    P = []
    steps = 0
    comparisons = 0
    i = 0

    while i < len(X_list):
        Y = np.array(X_list[i])
        fl = 0
        j = i + 1

        while j < len(X_list):
            steps += 1
            comparisons += 1

            Xj = np.array(X_list[j])
            if np.all(Y <= Xj) and np.any(Y < Xj):
                X_list.pop(j) 
            elif np.all(Xj <= Y) and np.any(Xj < Y):
                fl = 1
                Y = Xj
                X_list.pop(i)
                j = i + 1
                comparisons += 1
            else:
                j += 1

        P.append(Y.tolist())
        steps += 1

        if fl == 0:
            X_list.pop(i)
        else:
            i += 1
        steps += 1 

    end_time = time.time()
    elapsed_time = end_time - start_time

    results = {
        "Non-dominated points" : P,
        "Steps" : steps,
        "Comparisons" : comparisons,
        "Time (sec)" : elapsed_time
    }

    return results

def dominuje(A, B, comparisions):
    # Punkt A dominuje nad punktem B, jeśli każda współrzędna A jest <= każdej współrzędnej B
    # i przynajmniej jedna współrzędna A jest mniejsza niż odpowiadająca współrzędna B.
    czy_mniejszy = False  # Sprawdzenie, czy istnieje współrzędna mniejsza

    for a, b in zip(A, B):
        comparisions[0] += 1  # Zliczanie porównań
        if a > b:
            return False  # Jeśli którakolwiek współrzędna A jest większa, A nie dominuje B
        if a < b:
            czy_mniejszy = True  # Znaleziono przynajmniej jedną współrzędną mniejszą

    return czy_mniejszy

def filtracja_zdominowanych(X):
    start_time = time.time()
    n = len(X)
    usuniety = [False] * n
    P = [] 
    steps = 0
    comparisions = [0]  # Używamy listy, aby móc modyfikować licznik w funkcji dominuje

    for i in range(n):
        steps += 1
        if usuniety[i]:
            continue
        Y = X[i]

        for j in range(i + 1, n):
            steps += 1
            if usuniety[j]:
                continue

            if dominuje(Y, X[j], comparisions):
                usuniety[j] = True
            elif dominuje(X[j], Y, comparisions):
                usuniety[i] = True
                Y = X[j]

        if not usuniety[i]:
            P.append(Y)

        for k in range(i + 1, n):
            steps += 1
            if not usuniety[k] and dominuje(Y, X[k], comparisions):
                usuniety[k] = True

    end_time = time.time()

    elapsed_time = end_time - start_time
    
    results = {
        "Non-dominated points" : P,
        "Steps" : steps,
        "Comparisons" : comparisions[0],
        "Time (sec)" : elapsed_time
    }

    return results

def odleglosc_kwadratowa(A, B):
    return sum((a - b) ** 2 for a, b in zip(A, B))

def algorytm_punkt_idealny(X):
    steps = 0
    comparisions = [0]
    start_time = time.time()

    n = len(X)
    k = len(X[0])
    P = []

    xmin = [min(X[i][j] for i in range(n)) for j in range(k)]
    steps += 1

    d = [odleglosc_kwadratowa(xmin, X[j]) for j in range(n)]
    steps += 1

    J = sorted(range(n), key=lambda j: d[j])
    steps += 1

    M = n
    m = 0
    steps += 1

    usuniety = [False] * n
    while m < M:
        steps += 1
        aktualny_punkt = X[J[m]]

        if not usuniety[J[m]]:
            for i in range(n):
                if not usuniety[i] and dominuje(aktualny_punkt, X[i], comparisions):
                    usuniety[i] = True
            P.append(aktualny_punkt)
            steps += 1
            usuniety[J[m]] = True
        m += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    results = {
        "Non-dominated points" : P,
        "Steps" : steps,
        "Comparisons" : comparisions[0],
        "Time (sec)" : elapsed_time
    }

    return results


def run_benchmark(X):
    results = {}

    X_copy = X.copy().tolist()
    results1 = algorytm_bez_filtracji(X_copy)
    P1 = results1["Non-dominated points"]
    steps1 = results1["Steps"]
    comparisons1 = results1["Comparisions"]
    results["Algorytm bez filtracji"] = {"Steps": steps1, "Comparisons": comparisons1, "Non-dominated": len(P1), "Points": P1}


    X_copy = X.copy().tolist()
    results2 = filtracja_zdominowanych(X_copy)
    P2 = results2["Non-dominated points"]
    steps2 = results2["Steps"]
    comparisons2 = results2["Comparisions"]
    results["Algorytm z filtracją"] = {"Steps": steps2, "Comparisons": comparisons2, "Non-dominated": len(P2), "Points": P2}

    results3 = algorytm_punkt_idealny(X.copy())
    P3 = results3["Non-dominated points"]
    steps3 = results3["Steps"]
    comparisons3 = results3["Comparisions"]
    results["Algorytm z punktem idealnym"] = {"Steps": steps3, "Comparisons": comparisons3, "Non-dominated": len(P3), "Points": P3}

    return results