import time
import math
import random
import sys
import threading
import networkx as nx
import matplotlib.pyplot as plt


# WAŻNE ######
# W pliku wejsciowym wezly numerowane sa od zera, tj: pierwszy wezel trzeba wpisac jako 0, drugi jako 1 itd

def nextto_list(source_path):
    source = open(source_path, "r")
    first_line = source.readline().split(" ")
    nodes_quantity = int(first_line[0])
    edges_quantity = int(first_line[1])
    list = []

    for i in range(nodes_quantity):
        list.append([])

    for edge in range(edges_quantity):
        line = source.readline().split(" ")
        exit_node = int(line[0])
        entry_node = int(line[1])
        list[exit_node].append(entry_node)

    for i in range(nodes_quantity):
        list[i].sort()

    source.close()
    return list


# macierz sasiedztwa tworzenie
def create_neighbourhood_matrix(source_path):
    source = open(source_path, "r")
    first_line = source.readline().split(" ")
    nodes_quantity = int(first_line[0])
    edges_quantity = int(first_line[1])

    n_matrix = []
    for line in range(nodes_quantity):
        col = []
        for columns in range(nodes_quantity):
            col.append(0)
        n_matrix.append(col)

    for edge in range(edges_quantity):
        line = source.readline().split(" ")
        exit_node = int(line[0])
        entry_node = int(line[1])
        n_matrix[exit_node][entry_node] = 1
        n_matrix[entry_node][exit_node] = -1

    source.close()
    return n_matrix


# wypisywanie macierzy
def print_matrix(matrix):
    for i in matrix:
        print(i)


# wypisywanie grafu metoda dfs przy pomocy macierzy sasiedztwa(trzeba mu ja przekazac w parametrze)
visited = []  # macierz odwiedzin
stacklist = []
cycle = 0


# algorytmy dla maciezy sasiedztwa
def dfs_search_neighbourhood(node, res, node_quan, matrix):
    global visited
    global stacklist
    global cycle
    if visited[node] is False:
        res.append(node)
        visited[node] = True
        stacklist[node] = True
        for i in range(node_quan):
            if matrix[node][i] == 1 and visited[i] is False:
                dfs_search_neighbourhood(i, res, node_quan, matrix)
            elif matrix[node][i] == 1 and stacklist[i] is True:
                cycle = 1

    stacklist[node] = False


def dfs_neighbourhood(matrix, source_path):
    source = open(source_path, "r")
    line = source.readline().split(" ")
    global visited
    global stacklist
    global cycle

    nodes_quantity = int(line[0])
    edges_quantity = int(line[1])

    # tworzenie tablicy odwiedzonych wierzcholkow
    for i in range(nodes_quantity):
        visited.append(False)
    # tworzenie tablicy rekurencji
    for i in range(nodes_quantity):
        stacklist.append(False)

    # odwiedzanie i odkladanie na tablice do wypisania
    res = []
    iteration = 0
    while len(res) != nodes_quantity:
        dfs_search_neighbourhood(iteration, res, nodes_quantity, matrix)
        iteration += 1

    if cycle == 1:
        print("Graf zawiera cykl")

    # czyszczenie tablicy odwiedzonych do nastepnego uzycia
    visited = []
    stacklist = []
    cycle = 0
    return res


def del_neighbourhood(matrix, source_path):
    source = open(source_path, "r")
    line = source.readline().split(" ")

    nodes_quantity = int(line[0])
    edges_quantity = int(line[1])

    # tworzenie tablicy stopni wejscia wierzcholkow
    in_deg = []
    for i in range(nodes_quantity):
        in_deg.append(0)

    for i in range(nodes_quantity):
        for j in range(nodes_quantity):
            if matrix[j][i] == 1:
                in_deg[i] += 1

    res = []
    iterations = 0

    while len(res) != nodes_quantity:
        for i in range(nodes_quantity):
            if in_deg[i] == 0 and i not in res:
                iterations += 1
                res.append(i)
                for j in range(nodes_quantity):
                    if matrix[i][j] == 1:
                        in_deg[j] -= 1
                        matrix[i][j] = 0
                    if matrix[i][j] == -1:
                        matrix[i][j] = 0
        if iterations == 0:
            print("graf zawiera cykl, przerwanie sortowania")
            return
        iterations = 0

    return res


# algorytmy dla listy nastepnikow

def dfs_search_nextto(node, res, node_quan, matrix):
    global visited
    global stacklist
    global cycle
    if visited[node] is False:
        res.append(node)
        visited[node] = True
        stacklist[node] = True
        for i in matrix[node]:
            if visited[i] is False:
                dfs_search_nextto(i, res, node_quan, matrix)
            elif stacklist[i] is True:
                cycle = 1

    stacklist[node] = False


def dfs_nextto_list(matrix, source_path):
    source = open(source_path, "r")
    line = source.readline().split(" ")
    global visited
    global stacklist
    global cycle

    nodes_quantity = int(line[0])
    edges_quantity = int(line[1])

    # tworzenie tablicy odwiedzonych wierzcholkow
    for i in range(nodes_quantity):
        visited.append(False)
    # tworzenie tablicy rekurencji
    for i in range(nodes_quantity):
        stacklist.append(False)

        # odwiedzanie i odkladanie na tablice do wypisania
    res = []
    iteration = 0
    while len(res) != nodes_quantity:
        dfs_search_nextto(iteration, res, nodes_quantity, matrix)
        iteration += 1

    if cycle == 1:
        print("Graf zawiera cykl")

    # czyszczenie tablicy odwiedzonych do nastepnego uzycia
    visited = []
    stacklist = []
    cycle = 0
    return res


def del_nextto_list(matrix, source_path):
    source = open(source_path, "r")
    line = source.readline().split(" ")

    nodes_quantity = int(line[0])
    edges_quantity = int(line[1])

    # tworzenie tablicy stopni wejscia wierzcholkow
    in_deg = []
    for i in range(nodes_quantity):
        in_deg.append(0)

    for i in range(nodes_quantity):
        for j in matrix[i]:
            in_deg[j] += 1

    res = []
    iterations = 0

    while len(res) != nodes_quantity:
        for i in range(nodes_quantity):
            if in_deg[i] == 0 and i not in res:
                iterations += 1
                res.append(i)
                for j in matrix[i]:
                    in_deg[j] -= 1
        if iterations == 0:
            print("graf zawiera cykl, przerwanie sortowania")
            return
        iterations = 0

    return res


def create_graph(nodes, source):
    g = nx.gnr_graph(nodes, 0.5)
    name = str(source)
    plik = open(name, 'w')
    plik.write(str(nodes) + ' ')
    plik.write(str(nodes - 1) + '\n')
    for edge in g.edges:
        plik.write(str(edge[0]) + ' ')
        plik.write(str(edge[1]) + '\n')
    plik.close()


#wartosci testow
quantity = [500,700,900,1100,1300,1500,1700,1900,2100,2300,2500,3000,3500,10000,20000,30000,40000,50000,60000,70000,80000]

for i in quantity:
    create_graph(i, 'graf.txt')
    n_matrix = nextto_list("graf.txt")
    start = time.time()
    kahn = dfs_nextto_list(n_matrix, "graf.txt")
    stop = time.time()
    res = stop - start
    plik = open('wyniki_dfs_lista_nastepnikow.txt', 'a')
    plik.write(str(res) + '\n')
    plik.close()

