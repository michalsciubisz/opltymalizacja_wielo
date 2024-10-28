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

    # Tworzymy tablicę, która śledzi, czy dany punkt jest pomijany (usunięty)
    usuniety = [False] * n  # Na początku żaden element nie jest usunięty

    P = []  # Lista punktów niezdominowanych

    for i in range(n):
        if usuniety[i]:
            continue  # Jeśli punkt X[i] został już usunięty, pomijamy go

        Y = X[i]  # Bierzemy aktualny punkt Y

        # Przeglądamy wszystkie punkty po punkcie Y
        for j in range(i + 1, n):
            if usuniety[j]:
                continue  # Pomijamy punkt, jeśli już został oznaczony jako usunięty

            if dominuje(Y, X[j]):
                # Jeśli Y dominuje nad X[j], oznaczamy X[j] jako usunięty
                usuniety[j] = True
            elif dominuje(X[j], Y):
                # Jeśli X[j] dominuje nad Y, oznaczamy Y jako usunięty
                usuniety[i] = True
                Y = X[j]  # Zmieniamy Y na X[j]

        # Dodajemy Y do listy punktów niezdominowanych, jeśli nie został usunięty
        if not usuniety[i]:
            P.append(Y)

        # Filtracja: oznaczamy jako usunięte wszystkie X[k], takie że Y ≤ X[k]
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

if __name__ == '__main__':
    X = [(5,5), (3,6), (4,4), (5,3), (3,3),
(1,8), (3,4), (4,5), (3,10), (6,6), (4, 1), (3, 5)]
    result = filtracja_zdominowanych(X)
    print(result)
