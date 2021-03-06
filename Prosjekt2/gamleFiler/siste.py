import scipy
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import random


################ OPPGAVE 1 ################

def makeGrid(N):  # Lager en nxn matrise. N=lengde av polymer. n=N+2
    grid = np.zeros((N + 2, N + 2)).astype(np.int16)
    n = len(grid)
    grid[int(np.round(n / 2)), int(np.round(n / 2 - N / 2)): int(np.round(n / 2 - N / 2)) + N] = np.linspace(1, N,
                                                                                                             N).astype(
        np.int16)
    return grid


def findX(grid, x):
    pos = np.argwhere(grid == x)[0]
    col = pos[1]
    row = pos[0]
    return row, col


def rigid_rot(grid, x, lengde):
    if (x > math.floor((lengde / 2) + 1)):
        rot = grid.copy()
        rot[rot <= x] = 0

        rigid = grid.copy()
        rigid[rigid > x] = 0
    else:
        rot = grid.copy()
        rot[rot >= x] = 0

        rigid = grid.copy()
        rigid[rigid < x] = 0

    return rot, rigid


def isLegalTwist(twistedgrid, grid):
    if np.count_nonzero(grid) == np.count_nonzero(twistedgrid):
        bol = True
    else:
        bol = False
    return bol


def twist(grid, lengde, T):
    twist = False

    while (twist == False):
        x = np.random.randint(1, lengde + 1, None)

        n = np.random.randint(2, size=None)  # genererer clockwise

        rot, rigid = rigid_rot(grid, x, lengde)

        row_nonzero = np.count_nonzero(np.count_nonzero(rot, axis=1))  # teller rader med tall i
        col_nonzero = np.count_nonzero(np.count_nonzero(rot, axis=0))  # teller kolonner med tall i

        if row_nonzero > col_nonzero:
            side = row_nonzero
        else:
            side = col_nonzero

        row, col = findX(rigid, x)

        twister = rot[(row - side):(row + side + 1), (col - side):(col + side + 1)]
        twister = np.rot90(twister, (2 * n + 1))

        rot[(row - side):(row + side + 1), (col - side):(col + side + 1)] = twister
        twisted_matrix = np.add(rot, rigid)

        twist = isLegalTwist(twisted_matrix, grid)

    E2 = getEnergy(twisted_matrix)
    E1 = getEnergy(grid)

    r = np.random.uniform(0, 1)

    if E2 <= E1:
        return twisted_matrix
    elif r < np.exp(-beta(T) * (E2 - E1)):
        return twisted_matrix
    else:
        return grid


def twist_execute(antall_twists, lengde, grid, T):
    for i in range(np.round(antall_twists)):
        temp = grid
        twisted_matrix = twist(temp, lengde, T)
        grid = twisted_matrix

    return grid



################ OPPGAVE 2 ################


def U_ij(N):
    U = np.zeros((N + 1, N + 1))

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if abs(i - j) > 1:
                U[i][j] = np.random.uniform(-3.47 * 10 ** (-21), -10.4 * 10 ** (-21))
    return U


def d(T):
    return d_max * np.exp(-s * T)


def beta(T):
    return 1 / (1.38 * 10 ** (-23) * T)


def nearestNeighbours(grid, row, col):
    n = len(grid)
    E = 0
    if row + 1 < n:
        E = E + U[grid[row + 1, col]][grid[row, col]]
    if row - 1 >= 0:
        E = E + U[grid[row - 1, col]][grid[row, col]]
    if col + 1 < n:
        E = E + U[grid[row, col + 1]][grid[row, col]]
    if col - 1 >= 0:
        E = E + U[grid[row, col - 1]][grid[row, col]]
    return E


# dobbel for løkke, ytre løkke der T går fra 0 til 1500 K, og indreløkke kjører d(T) twists ved hver temp.

def getEnergy(polymer):  # finner energien til hele polymeret
    totalEnergy = 0
    for x in range(1, N+1):  # Går igjennom lengden på polymeret
        row, col = findX(polymer, x)
        totalEnergy += 0.5 * nearestNeighbours(polymer, row, col)
    return totalEnergy


def plotEnergy(grid):
    N = len(grid) - 2
    eps = np.zeros((Nt, d_max))
    # L = np.zeros((Nt, d_max))
    eps[0][0] = 0
    # L[0][0] = N
    for i in range(0, Nt):
        print('loop ', i + 1, ' av ', Nt)
        grid = makeGrid(N)
        temp = T_arr[i]
        for j in range(1, int(d(temp))):
            E = getEnergy(grid)

            copyGrid = twist(grid, N, temp)
            Enew = getEnergy(copyGrid)

            if Enew < E:
                grid = copyGrid
                E = Enew
            elif np.random.uniform(0, 1) < np.exp(-beta(temp) * (Enew - E)):
                grid = copyGrid

            eps[i][j] = E
            # L[i][j] = findDiameter(grid, N)

    energyList = np.zeros(Nt)
    for i in range(Nt):
        energyList[i] = np.mean(eps[i][:int(d(T_arr[i]))])

    plt.figure()
    plt.plot(T_arr, energyList, label='%i monomerer' % N)
    plt.title(r'Gjennomsnittsenergi sfa. temperatur')
    plt.xlabel(r'$T$')
    plt.ylabel(r'$\langle E \rangle$')
    plt.legend()
    plt.savefig('2,1plotEnergy.pdf')
    plt.show()


def plotBindingEnergy(grid):

    #T = 1e-7
    T = 500
    num_of_twists = 5000
    E = np.zeros(num_of_twists)
    twists = np.zeros(num_of_twists)

    for twist in range(1, num_of_twists, 1):
        polymer = twist_execute(twist, N, grid, T)
        E = np.append(E, (getEnergy(polymer)))
        twists = np.append(twists, twist)
        print('twist %i of %i' % (twist, num_of_twists))

    plt.plot(twists, E, label=r'$T=%i$ K' % (round(T)))
    plt.title('Bindingsenergi sfa. antall tvister')  # TITTEL
    plt.xlabel('Antall tvister')
    plt.ylabel(r'$E$')
    plt.legend()
    plt.savefig('2,2plotBindingEnergy_%iK.pdf' % (round(T)))  # NAVN
    plt.show()



################ OPPGAVE 4 ################


def gradualCooling(polymer):
    temp_start = 1500
    temp_end = 0
    temp_step = -30
    num_of_twists = 600

    x = round(temp_start / -temp_step)
    E = np.zeros(x * num_of_twists)
    twists = range(0, x * num_of_twists)
    i = 0

    # Lagrer energien for hver tvist ved gitt temperatur T.
    for T in range(temp_start, temp_end, temp_step):  # T går fra 1500 K til 0 K med steglengde -30 K.
        for tw in range(1, num_of_twists + 1):  # tw(ist) går fra 1 til 600.
            polymer = twist_execute(1, N, polymer, T)
            E[i] = getEnergy(polymer)
            i += 1
        print('T = ', T)

    plt.plot(twists, E, linewidth=.15, label='%i monomerer' %N)
    plt.title(r'Energi sfa. antall tvister, nedkjøling', fontsize=10)
    plt.xlabel(r'Antall tvister')
    plt.ylabel(r'$E$')
    plt.legend()
    plt.savefig('4,1gradualCooling%imon.pdf' %N)
    plt.show()


def gradualCoolingMeanEnergy(polymer):
    start = time.time()

    temp_start = 1500
    temp_end = 0
    temp_step = -30
    num_of_twists = 600

    E_temp = np.zeros(num_of_twists)  # Energi for en gitt T.
    x = round(temp_start / -temp_step)
    E_mean = np.zeros(x)
    temp_axis = range(temp_start, temp_end, temp_step)
    i = j = 0

    # Lagrer energien for hver tvist ved gitt temperatur T.
    for T in range(temp_start, temp_end, temp_step):  # T går fra 1500 K til 0 K med steglengde -30 K.
        for tw in range(1, num_of_twists + 1):  # tw(ist) går fra 1 til 600.
            polymer = twist_execute(1, N, polymer, T)
            E_temp[i] = getEnergy(polymer)
            i += 1
        E_mean[j] = np.average(E_temp)
        i = 0
        print('T = ', T)
        j += 1

    plt.plot(temp_axis, E_mean, linewidth=1, label='%i monomerer' %N)
    plt.title(r'Gjennomsnittsenergi sfa. temperatur, nedkjøling', fontsize=10)
    plt.xlabel(r'$T$')
    plt.ylabel(r'$\langle E \rangle$')
    plt.legend()
    plt.savefig('4,2gradualCoolingMeanEnergy%imon.pdf' %N)
    plt.show()


start = time.time()
N = 15
s = 0.004
Nt = 50
d_max = 30000
T_end = 1500
T_arr = np.arange(1e-7, T_end, T_end / Nt)
U = U_ij(N)
