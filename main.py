import sys
# import copy


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
        # print(self.start)
        #verificarea corectitudinii starii de start
        # print(self.scop)


    def testeazaScop(self, nodCurent):
        return nodCurent.info == self.scop


    def calculeaza_cost_linii(self, mat, matrice):
        # print(matrice)
        # print(len(mat), len(matrice[0]))
        return len(matrice[0])/len(mat)


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
        return 1+ cost/(len(mat))



    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        matrice = nodCurent.info
        if len(matrice) > len(self.scop):
            for i in range(len(matrice)):
                for j in range(i, len(matrice)):
                    succ = matrice[i:j+1]
                    if succ == matrice:
                        continue
                    rest = matrice[:i] + matrice[j+1:]
                    cost = self.calculeaza_cost_linii(rest, matrice)
                    # print (cost)
                    listaSuccesori.append(NodParcurgere(succ, nodCurent, nodCurent.g + cost))
        else:
            for i in range(len(matrice[0])):
                for j in range(i, len(matrice[0])):
                    succ = []
                    rest = []
                    for linie in matrice:
                        succ.append(linie[i:j+1])
                        rest.append(linie[:i] + linie[j+1:])
                    if succ == matrice:
                        continue
                    cost = self.calculeaza_cost_coloane(rest)
                    # print (rest, cost)
                    listaSuccesori.append(NodParcurgere(succ, nodCurent, nodCurent.g + cost))

        return listaSuccesori


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
lista = graf.genereazaSuccesori(c)
print (*lista, sep = '\n')
lista = graf.genereazaSuccesori(d)
print (*lista, sep = '\n')