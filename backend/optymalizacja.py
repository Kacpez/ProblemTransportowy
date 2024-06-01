import numpy as np
import copy
import random
INF=100**4
def generuj_liste(oczekiwana_suma,dlugosc):
    lista = [random.randint(50, 150) for _ in range(dlugosc)]
    roznica = oczekiwana_suma - sum(lista)
        # Dodanie lub odjęcie rożnicy do jednego z elementów listy
    lista[random.randint(0, dlugosc-1)] += roznica
    return lista

def wypisywanie_macierzy(macierz):
    for i in macierz:
        for j in i:
            print("%3s" %(j),end=" ")
        print()

def oblicznie_kosztu(macierz_kosztu,macierz_wynikowa):
    koszt_sumaryczny=0
    N,M=macierz_kosztu.shape
    for i in range(N):
        for j in range(M):
            koszt_sumaryczny+=macierz_kosztu[i][j]*macierz_wynikowa[i][j]
    return koszt_sumaryczny

# algorytm transportowy
# metoda kata polnocno-zachodnigo

def pzk_metoda(macierz_kosztu,popyt,podaz):
    if not macierz_kosztu.any() or not popyt.any() or not podaz.any():
        raise ValueError("Empty matrix, demand, or supply list")
    if sum(popyt) != sum(podaz):
        raise ValueError("Demand and supply sums do not match")
    N,M=macierz_kosztu.shape
    zera=[[0]*M for i in range(N)]
    macierz_zer= np.array(zera)
    popyt_obecny = copy.copy(popyt)
    podaz_obecna = copy.copy(podaz)
    i=0
    j=0
    while(i<N and j<M):
        if popyt_obecny[i]>=podaz_obecna[j]:
            macierz_zer[i][j]=podaz_obecna[j]
            popyt_obecny[i]-=podaz_obecna[j]
            j+=1
        else :
            macierz_zer[i][j]=popyt_obecny[i]
            podaz_obecna[j]-=popyt_obecny[i]
            i+=1
    return macierz_zer

#metoda najmnieszego elementu macierzy
def nem_metoda(macierz_kosztu,popyt,podaz):
    if not macierz_kosztu.any() or not popyt.any() or not podaz.any():
        raise ValueError("Empty matrix, demand, or supply list")
    if sum(popyt) != sum(podaz):
        raise ValueError("Demand and supply sums do not match")
    N,M=macierz_kosztu.shape
    macierz_kosztu_obecna=copy.copy(macierz_kosztu)
    zera=[[0]*M for i in range(N)]
    macierz_zer= np.array(zera)
    popyt_obecny = copy.copy(popyt)
    podaz_obecna = copy.copy(podaz)

    while np.sum(podaz_obecna)>0 and np.sum(popyt_obecny)>0:
        i,j = np.unravel_index(macierz_kosztu_obecna.argmin(), macierz_kosztu_obecna.shape)
        ilosc = min(popyt_obecny[i], podaz_obecna[j])
        popyt_obecny[i]-=ilosc
        podaz_obecna[j]-=ilosc
        macierz_zer[i][j]=ilosc
        if popyt_obecny[i] == 0:
            macierz_kosztu_obecna[i, :] = INF
        if podaz_obecna[j] == 0:
            macierz_kosztu_obecna[:, j] = INF

    return macierz_zer

#metoda vogela #########################################################################

def roznica(macierz):
    roznica_wiersz = [np.partition(row, 1)[1] - np.partition(row, 0)[0] if np.count_nonzero(row != np.inf) > 1 else 0 for row in macierz]
    roznica_kolumna = [np.partition(col, 1)[1] - np.partition(col, 0)[0] if np.count_nonzero(col != np.inf) > 1 else 0 for col in np.array(macierz).T]
    return roznica_wiersz, roznica_kolumna

def vam_metoda(macierz_kosztu, popyt, podaz):
    if not macierz_kosztu.any():
        raise ValueError("Empty matrix")
    if sum(popyt) != sum(podaz):
        raise ValueError("Demand and supply sums do not match")

    N, M = macierz_kosztu.shape
    zera = [[0] * M for _ in range(N)]
    macierz_zer = np.array(zera)
    popyt_obecny = copy.copy(popyt)
    podaz_obecna = copy.copy(podaz)
    macierz_kosztu_obecna = copy.copy(macierz_kosztu)
    popyt_obecny = np.array(popyt_obecny)
    podaz_obecna = np.array(podaz_obecna)
    if popyt_obecny.size==0 or podaz_obecna.size==0:
        raise ValueError("Empty demand or supply list")
    
    while np.any(popyt_obecny > 0) or np.any(podaz_obecna > 0):
        roznica_wiersz, roznica_kolumna = roznica(macierz_kosztu_obecna)
        max1 = max(roznica_wiersz)
        max2 = max(roznica_kolumna)

        if max1==0 and max2==0:
            break
    
        if max1 >= max2:
            wiersz_index = np.argmax(roznica_wiersz)
            kolumna_index = np.argmin(macierz_kosztu_obecna[wiersz_index])
        else:
            kolumna_index = np.argmax(roznica_kolumna)
            wiersz_index = np.argmin(macierz_kosztu_obecna[:, kolumna_index])

        ilosc = min(popyt_obecny[wiersz_index], podaz_obecna[kolumna_index])
        macierz_zer[wiersz_index][kolumna_index] = ilosc
        popyt_obecny[wiersz_index] -= ilosc
        podaz_obecna[kolumna_index] -= ilosc

        if popyt_obecny[wiersz_index] == 0:
            macierz_kosztu_obecna[wiersz_index, :] = np.iinfo(np.int32).max
        if podaz_obecna[kolumna_index] == 0:
            macierz_kosztu_obecna[:, kolumna_index] = np.iinfo(np.int32).max

    return macierz_zer




