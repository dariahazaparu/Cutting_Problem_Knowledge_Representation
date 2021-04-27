import sys
import time
import stopit
# from multiprocessing import Pool, TimeoutError


class NodParcurgere:
    def __init__(self, id, info, parinte, cost=0, h=0):
        self.id = id
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h  # euristica
        self.f = self.g + self.h  # suma

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Lungime: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        for linie in self.info:
            sir += "".join([str(elem) for elem in linie]) + "\n"
        return sir

    def __str__(self):
        sir = "Nodul " + str(self.id) + ':\n'
        for linie in self.info:
            sir += "".join([str(elem) for elem in linie]) + "\n"
        return sir


class Graph:
    def __init__(self, initial, finish):
        self.start = NodParcurgere(1, initial, None)
        self.scop = finish
        self.eur1 = len(initial) - len(finish) if len(initial) - len(finish) > 0 else 1
        self.eur2 = len(initial) - len(finish) + len(initial[0]) - len(finish[0]) \
            if len(initial) - len(finish) + len(
            initial[0]) - len(finish[0]) > 0 else 1

    def testeazaScop(self, nodCurent):
        return nodCurent.info == self.scop

    def calculeaza_cost_linii(self, succ, matrice):
        return len(matrice[0]) / len(succ)

    def calculeaza_cost_coloane(self, mat):
        cost = 0
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if i != len(mat) - 1:
                    if mat[i][j] != mat[i + 1][j]:
                        cost += 1
                if j != len(mat[len(mat) - 1]) - 1:
                    if mat[i][j] != mat[i][j + 1]:
                        cost += 1
        return 1 + cost / (len(mat[0]))

    def calculeaza_euristica_1(self, cost):
        return cost * self.eur1

    def calculeaza_euristica_2(self, cost):
        return cost * (1 + self.eur2)

    def calculeaza_euristica_3(self, cost, rest):
        return cost * len(rest)

    def verifica_succesor(self, matrice):
        linie_scop = self.scop[0]
        # print(linie_scop)
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if matrice[i][j] == linie_scop[0] and len(linie_scop) - j >= 0:
                    index = 0
                    for k in range(j, len(matrice[i])):
                        if index < len(linie_scop):
                            if matrice[i][k] == linie_scop[index]:
                                index += 1
                        else:
                            break
                    if index == len(linie_scop) - 1:
                        return True
        return False

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        global ind
        listaSuccesori = []
        matrice = nodCurent.info
        for i in range(len(matrice)):
            for j in range(i, len(matrice)):
                succ = matrice[i:j + 1]
                if succ == matrice:
                    continue
                rest = matrice[:i] + matrice[j + 1:]
                cost = self.calculeaza_cost_linii(succ, matrice)
                eur = 1
                if tip_euristica == "euristica 1":
                    eur = self.calculeaza_euristica_1(cost)
                if tip_euristica == "euristica 2":
                    eur = self.calculeaza_euristica_2(cost)
                if tip_euristica == "euristica 3":
                    eur = self.calculeaza_euristica_3(cost, succ)
                ind += 1
                if self.verifica_succesor(rest):
                    listaSuccesori.append(NodParcurgere(ind, rest, nodCurent, nodCurent.g + cost, eur))

        for i in range(len(matrice[0])):
            for j in range(i, len(matrice[0])):
                succ = []
                rest = []
                for linie in matrice:
                    succ.append(linie[i:j + 1])
                    rest.append(linie[:i] + linie[j + 1:])
                if succ == matrice:
                    continue
                cost = self.calculeaza_cost_coloane(succ)
                eur = 1
                if tip_euristica == "euristica 1":
                    eur = self.calculeaza_euristica_1(cost)
                if tip_euristica == "euristica 2":
                    eur = self.calculeaza_euristica_2(cost)
                if tip_euristica == "euristica 3":
                    eur = self.calculeaza_euristica_3(cost, succ)
                ind += 1
                if self.verifica_succesor(rest):
                    listaSuccesori.append(NodParcurgere(ind, rest, nodCurent, nodCurent.g + cost, eur))

        return listaSuccesori


def uniformCost(gr, nrSolutiiCautate=1):
    print("UCS running...")
    global ind
    ind = 1

    c = [gr.start]
    output = "Uniform Cost\n\n"
    t = time.time()
    MAX = 0
    while len(c) > 0:

        ln = len(c)
        if ln > MAX:
            MAX = ln

        nodCurent = c.pop(0)

        if gr.testeazaScop(nodCurent):
            output += "*Solutie*\n"
            l = nodCurent.obtineDrum()
            for nod in l:
                output += str(nod) + '\n'
            output += "Cost: " + str(nodCurent.g) + '\n'
            output += "Lungime: " + str(len(l)) + '\n\n'
            output += "\n-------------------------\n"
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                e = time.time()
                output += "Timp de executie: " + str(e - t) + " secunde\n"
                output += "Numar de noduri existente la un moment dat: " + str(MAX) + '\n'
                output += "Total noduri: " + str(ind) + '\n'
                out(output, "ucs.txt")
                print("UCS finished")
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def aStar(gr, nrSolutiiCautate=1, tip_euristica="euristica banala"):
    print(f"A* {tip_euristica} running...")

    global ind
    ind = 1
    c = [gr.start]
    output = f"A* {tip_euristica}\n\n"
    t = time.time()
    MAX = 0

    while len(c) > 0:

        ln = len(c)
        if ln > MAX:
            MAX = ln
        nodCurent = c.pop(0)

        if gr.testeazaScop(nodCurent):
            output += "*Solutie*\n"
            l = nodCurent.obtineDrum()
            for nod in l:
                output += str(nod) + '\n'
            output += "Cost: " + str(nodCurent.g) + '\n'
            output += "Lungime: " + str(len(l)) + '\n\n'
            output += "\n-------------------------\n"
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                e = time.time()
                output += "Timp de executie: " + str(e - t) + " secunde\n"
                output += "Numar de noduri existente la un moment dat: " + str(MAX) + '\n'
                output += "Total noduri: " + str(ind) + '\n'
                fisier = "astar.txt"
                if tip_euristica == "euristica 1":
                    fisier = "astareur1.txt"
                if tip_euristica == "euristica 2":
                    fisier = "astareur2.txt"
                if tip_euristica == "euristica 3":
                    fisier = "astareur3.txt"
                out(output, fisier)
                print(f"A* {tip_euristica} finished")
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].f > s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def aStarOpt(gr, tip_euristica="euristica banala"):
    print(f"A* opt {tip_euristica} running...")

    global ind
    ind = 1

    output = f"A* optimizat {tip_euristica}\n\n"
    t = time.time()
    MAX = 0
    l_open = [gr.start]

    l_closed = []
    while len(l_open) > 0:

        ln = len(l_open) + len(l_closed)
        if ln > MAX:
            MAX = ln

        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeazaScop(nodCurent):
            output += "*Solutie*\n"
            l = nodCurent.obtineDrum()
            for nod in l:
                output += str(nod) + '\n'
            output += "Cost: " + str(nodCurent.g) + '\n'
            output += "Lungime: " + str(len(l)) + '\n'
            e = time.time()
            output += "Timp de executie: " + str(e - t) + " secunde\n"
            output += "Numar de noduri existente la un moment dat: " + str(MAX) + '\n'
            output += "Total noduri: " + str(ind) + '\n'
            fisier = "astaropt.txt"
            if tip_euristica == "euristica 1":
                fisier = "astaropteur1.txt"
            if tip_euristica == "euristica 2":
                fisier = "astaropteur2.txt"
            if tip_euristica == "euristica 3":
                fisier = "astartopteur3.txt"
            out(output, fisier)
            print(f"A* opt {tip_euristica} finished")
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)


def idaStar(gr, nrSolutiiCautate=1, tip_euristica="euristica banala"):
    print(f"IDA* {tip_euristica} running...")

    global ind
    ind = 1

    nodStart = gr.start
    limita = nodStart.f
    fisier = "idastar.txt"
    if tip_euristica == "euristica 1":
        fisier = "idastareur1.txt"
    if tip_euristica == "euristica 2":
        fisier = "idastareur2.txt"
    if tip_euristica == "euristica 3":
        fisier = "idastareur3.txt"
    f = open(fisier, "w")

    f.write(f"IDA* {tip_euristica}\n\n")
    t = time.time()
    MAX = 0

    while True:
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, tip_euristica, limita, nrSolutiiCautate, f, t, MAX)
        if rez == "gata":
            break
        if rez == float('inf'):
            f.write("Nu exista solutii!")
            break
        limita = rez

    f.close()
    print(f"IDA* {tip_euristica} finished")


def construieste_drum(gr, nodCurent, tip_euristica, limita, nrSolutiiCautate, f, t, MAX):
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeazaScop(nodCurent) and nodCurent.f == limita:
        f.write("*Solutie*\n")
        l = nodCurent.obtineDrum()
        for nod in l:
            f.write(str(nod) + '\n')
        f.write("Cost: " + str(nodCurent.g) + '\n')
        f.write("Lungime: " + str(len(l)) + '\n\n')
        f.write("Limita: " + str(limita) + '\n')

        f.write("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            e = time.time()
            f.write("Timp de executie: " + str(e - t) + " secunde\n")
            f.write("Numar de noduri existente la un moment dat: " + str(MAX) + '\n')
            f.write("Total noduri: " + str(ind) + '\n')
            return 0, "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, tip_euristica, limita, nrSolutiiCautate, f, t, MAX)
        if rez == "gata":
            return 0, "gata"
        if rez < minim:
            minim = rez
    return nrSolutiiCautate, minim


def verifica(matrice):
    cont = len(matrice[0])
    for linie in matrice:
        if len(linie) != cont:
            return False
    return True


def read():
    fisier = input("Nume fisier input:")
    f = open(fisier, "r")

    k = int(input("Numar solutii cautate: "))
    line = f.readline()
    alls = []
    while line:
        alls.append([l for l in line])
        line = f.readline()
    f.close()

    begin = []
    index = 0
    for i in range(len(alls)):
        if alls[i] == ['\n']:
            index = i
            break
        else:
            begin.append(alls[i])

    for line in begin:
        line.remove(line[-1])

    end = []
    for i in range(index + 1, len(alls)):
        end.append(alls[i])

    for i in range(len(end) - 1):
        end[i].remove(end[i][-1])

    timeout = int(input("Timeout: "))
    if verifica(begin) and verifica(end):
        return k, begin, end, timeout
    print("Eroare la citire.")
    sys.exit(0)


def out(output, fisier):
    f = open(fisier, "w")
    f.write(output)
    f.close()


def main_without_time():

    k, initial, final, time_out = read()
    graf = Graph(initial, final)

    uniformCost(graf, k)

    aStar(graf, k)
    aStar(graf, k, "euristica 1")
    aStar(graf, k, "euristica 2")
    aStar(graf, k, "euristica 3")

    aStarOpt(graf)
    aStarOpt(graf, "euristica 1")
    aStarOpt(graf, "euristica 2")
    aStarOpt(graf, "euristica 3")

    idaStar(graf, k)
    idaStar(graf, k, "euristica 1")
    idaStar(graf, k, "euristica 2")
    idaStar(graf, k, "euristica 3")


if __name__ == '__main__':
    main_without_time()
