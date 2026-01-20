import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        #commint and push di prova

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        pass

    def build_graph(self, n_alb):
        artisti, ar_al = DAO.get_artits_album(int(n_alb))
        for a in artisti:
            self._graph.add_node(a)
        album_generi = DAO.get_generi()
        artisti_generi = {}
        for a in self._graph.nodes():
            set_generi = set()
            for album in ar_al[a.id]['album']:
                for genere in album_generi[album]['generi']:
                    set_generi.add(genere)
                artisti_generi[a.id] = set_generi
        for v in self._graph.nodes():
            for u in self._graph.nodes():
                if v != u:
                    lista_comuni = []
                    for g1 in artisti_generi[v.id]:
                        for g2 in artisti_generi[u.id]:
                            if g1 == g2:
                                lista_comuni.append(g1)
                    if lista_comuni:
                        self._graph.add_edge(v, u, peso=len(lista_comuni))

    def artisti_collegati(self, v):
        vicini = []
        for vicino in self._graph.neighbors(v):
            peso = self._graph[v][vicino]['peso']
            vicini.append((vicino, peso))
        return sorted(vicini, key=lambda x: x[0].id)

    def percorso(self, nodo_in, durata_min, lunghezza_cammino):

        self.vincolo_lunghezza = int(lunghezza_cammino)
        self.vincolo_in = nodo_in
        self.best_path = []
        self.best_score = 0
        self.vincolo_durata_min = durata_min # vincolo durata min da gestire col databese perchè non ho pèreso milliseconds
        parziale = [nodo_in]


        peso_iniziale = 0
        durata_da_confrontare = 0

        self.ricorsione_percorso(parziale,durata_da_confrontare, peso_iniziale)

        return self.best_path, self.best_score

    def ricorsione_percorso(self, parziale,durata_da_confrontare, score_corrente):

        if self.vincolo_lunghezza == len(parziale):
                if durata_da_confrontare >= self.vincolo_durata_min:
                    self.best_score = score_corrente
                    self.best_path = list(parziale)
                return
        last = parziale[-1]
        for vicino in self._graph.neighbors(last):
            parziale.append(vicino)
            peso = self._graph[last][vicino]['peso']
            #durata_da_confrontare = ...            # prendo la durata_da_confrontare
            self.ricorsione_percorso(parziale, durata_da_confrontare, score_corrente + peso)
            parziale.pop(vicino)







