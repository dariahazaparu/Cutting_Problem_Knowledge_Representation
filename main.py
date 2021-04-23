import sys
import time


class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info=info
        self.parinte=parinte #parintele din arborele de parcurgere
        self.g=cost #consider cost=1 pentru o mutare
        self.h=h #euristica
        self.f=self.g+self.h #suma


    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l


    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
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
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False


    def __repr__(self):
        # sir = ""
        # sir += str(self.info)
        # return (sir)
        sir = ""
        for linie in self.info:
            sir += "".join([str(elem) for elem in linie]) + "\n"
        return sir

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += "".join([str(elem) for elem in linie]) + "\n"
        return sir

class Graph: #graful problemei
    def __init__(self, initial, finish):
        self.start = NodParcurgere(initial, None)
        self.scop = finish
        self.eur = len(initial) - len(finish) if len(initial) - len(finish) > 0 else 1
        # print(self.start)
        #verificarea corectitudinii starii de start
        # print(self.scop)


    def testeazaScop(self, nodCurent):
        return nodCurent.info == self.scop


    def calculeaza_cost_linii(self, succ, matrice):
        return len(matrice[0])/len(succ)


    def calculeaza_cost_coloane(self, mat):
        cost = 0
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if i != len(mat) - 1:
                    if mat[i][j] != mat[i+1][j]:
                        cost += 1
                if j != len(mat[len(mat)-1]) - 1:
                    if mat[i][j] != mat[i][j+1]:
                        cost += 1
        return 1+ cost/(len(mat[0]))


    def calculeaza_euristica_banala(self, cost, mat):
        return cost/self.eur


    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        matrice = nodCurent.info
        for i in range(len(matrice)):
            for j in range(i, len(matrice)):
                succ = matrice[i:j+1]
                if succ == matrice:
                    continue
                rest = matrice[:i] + matrice[j+1:]
                cost = self.calculeaza_cost_linii(succ, matrice)
                eur = self.calculeaza_euristica_banala(cost, rest)
                # print (eur)
                listaSuccesori.append(NodParcurgere(rest, nodCurent, nodCurent.g + cost, eur))

        for i in range(len(matrice[0])):
            for j in range(i, len(matrice[0])):
                succ = []
                rest = []
                for linie in matrice:
                    succ.append(linie[i:j+1])
                    rest.append(linie[:i] + linie[j+1:])
                if succ == matrice:
                    continue
                cost = self.calculeaza_cost_coloane(succ)
                eur = self.calculeaza_euristica_banala(cost, rest)
                # print (eur)
                listaSuccesori.append(NodParcurgere(rest, nodCurent, nodCurent.g + cost, eur))

        return listaSuccesori


def uniformCost(gr, nrSolutiiCautate=1):
    c = [gr.start]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeazaScop(nodCurent):
            print("Solutie: ", end="\n")
            nodCurent.afisDrum(True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
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


def aStar(gr, nrSolutiiCautate=1):
    c = [gr.start]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeazaScop(nodCurent):
            print("Solutie: ", end="\n")
            nodCurent.afisDrum(True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
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


def aStarOpt(gr):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open = [gr.start]

    # l_open contine nodurile candidate pentru expandare

    # l_closed contine nodurile expandate
    l_closed = []
    while len(l_open) > 0:
        # print("Coada actuala: " + str(l_open))
        # input()
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="\n")
            nodCurent.afisDrum()
            print("\n----------------\n")
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez crescator dupa f
                # daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)


def ida_star(gr, nrSolutiiCautate):
    nodStart = gr.start
    limita = nodStart.f
    while True:

        print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate)
        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu exista solutii!")
            break
        limita = rez
        print(">>> Limita noua: ", limita)


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate):
    print("A ajuns la: ", nodCurent)
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeazaScop(nodCurent) and nodCurent.f == limita:
        print("Solutie: ")
        nodCurent.afisDrum(True)
        print(limita)
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0, "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate)
        if rez == "gata":
            return 0, "gata"
        print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            print("Noul minim: ", minim)
    return nrSolutiiCautate, minim


def read():

    # fisier = input("Nume fisier input:")
    # f = open(fisier, "r")
    f = open("input1.txt", "r")

    line = f.readline()
    alls = []
    while line:
        alls.append([l for l in line])
        line = f.readline()
    f.close()

    begin = []
    ind = 0
    for i in range(len(alls)):
        if alls[i] == ['\n']:
            ind = i
            break
        else:
            begin.append(alls[i])

    for line in begin:
        line.remove(line[-1])

    end = []
    for i in range(ind+1, len(alls)):
        end.append(alls[i])

    for i in range(len(end)-1):
        end[i].remove(end[i][-1])

    timeout = int(end[-1][0])
    end.remove(end[-1])
    return begin, end, timeout


def out():
    # fisier = input("Nume fisier output:")
    # f = open(fisier, "w")
    f = open("output1.txt", "w")
    f.close()


initial, final, timeout = read()
initial2 = initial[:2]
c = NodParcurgere(initial, None)
d = NodParcurgere(initial2, c)

graf = Graph(initial, final)
t = time.time()
uniformCost(graf, 4)
e = time.time()
print (e-t)
print ("###############################################")
t = time.time()
aStar(graf, 4)
e = time.time()
print (e-t)
print ("###############################################")
t = time.time()
aStar(graf, 4)
e = time.time()
print (e-t)
print ("###############################################")
t = time.time()
ida_star(graf, 1)
e = time.time()
print (e-t)
