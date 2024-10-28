def algorytm_bez_filtracji(X):
    P = []
    i = 0
    while i < len(X):
        Y = X[i]
        fl = 0
        j = i + 1
        while j < len(X):
            if Y[0] <= X[j][0] and Y[1] <= X[j][1]:
                X.pop(j)
            elif X[j][0] <= Y[0] and X[j][1] <= Y[1]:
                X.pop(i)
                fl = 1
                break
            else:
                j += 1
        
        if fl == 0:
            P.append(Y)
            i += 1
        else:
            fl = 0
    return P

def dominuje(A, B):
    # Punkt A dominuje nad punktem B, jeśli każda współrzędna A jest <= każdej współrzędnej B
    # i przynajmniej jedna współrzędna A jest mniejsza niż odpowiadająca współrzędna B.
    czy_mniejszy = False  # Sprawdzenie, czy istnieje współrzędna mniejsza

    for a, b in zip(A, B):
        if a > b:
            return False  # Jeśli którakolwiek współrzędna A jest większa, A nie dominuje B
        if a < b:
            czy_mniejszy = True  # Znaleziono przynajmniej jedną współrzędną mniejszą

    return czy_mniejszy

def filtracja_zdominowanych(X):
    n = len(X)
    usuniety = [False] * n
    P = [] 
    for i in range(n):
        if usuniety[i]:
            continue
        Y = X[i]

        for j in range(i + 1, n):
            if usuniety[j]:
                continue

            if dominuje(Y, X[j]):
                usuniety[j] = True
            elif dominuje(X[j], Y):
                usuniety[i] = True
                Y = X[j]

        if not usuniety[i]:
            P.append(Y)

        for k in range(i + 1, n):
            if not usuniety[k] and dominuje(Y, X[k]):
                usuniety[k] = True

    return P

def odleglosc_kwadratowa(A, B):
    return sum((a - b) ** 2 for a, b in zip(A, B))

def algorytm_punkt_idealny(X):
    n = len(X)
    k = len(X[0])
    P = []
    xmin = [min(X[i][j] for i in range(n)) for j in range(k)]
    d = [odleglosc_kwadratowa(xmin, X[j]) for j in range(n)]
    J = sorted(range(n), key=lambda j: d[j])

    M = n
    m = 0

    usuniety = [False] * n
    while m < M:
        aktualny_punkt = X[J[m]]

        if not usuniety[J[m]]:
            for i in range(n):
                if not usuniety[i] and dominuje(aktualny_punkt, X[i]):
                    usuniety[i] = True
            P.append(aktualny_punkt)
            usuniety[J[m]] = True
        m += 1

    return P