import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_artist = None

    def handle_create_graph(self, e):
        if self._view.txtNumAlbumMin.value == "":
            self._view.show_alert("Selezionare un numero di alb")
            return
        self._model.build_graph(self._view.txtNumAlbumMin.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato: {self._model._graph.number_of_nodes()} nodi (artisti), {self._model._graph.number_of_edges()} archi")
        )
        self.populate_dd_artist()
        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False

        self._view.update_page()

    def populate_dd_artist(self):
        artisti = self._model._graph.nodes()
        self._view.ddArtist.options.clear()
        for a in artisti:
            option = ft.dropdown.Option(text=a.name, data=a)
            self._view.ddArtist.options.append(option)
        self._view.update_page()
    def get_selected_artist(self, e):
        selected_option = e.control.value
        if selected_option is None:
            self._current_artist = None
            return
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break
        self._current_artist = found

    def handle_connected_artists(self, e):
        if self._current_artist is None:
            self._view.show_alert("Selezionare un artista'")
            return
        artisti_collegati = self._model.artisti_collegati(self._current_artist)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Artisti direttamente collegati all'artista {self._current_artist.id}, {self._current_artist.name}"))
        for art, peso in artisti_collegati:
            self._view.txt_result.controls.append(
                ft.Text(
                    f"{art.id}, {art.name} - Numero generi in comune: {peso}")
            )
        self._view.update_page()


    def cammino_artista(self,e):
        if self._current_artist is None:
            self._view.show_alert("Selezionare un artista'")
            return
        elif self._view.txtMinDuration.value == "" or  float(self._view.txtMinDuration.value) <= 0:
            self._view.show_alert("Selezionare un numero di durata valido")
            return
        elif self._view.txtMaxArtists.value == "" or int(self._view.txtMaxArtists.value) < 1 or int(self._view.txtMaxArtists.value) > self._model._graph.number_of_nodes():
            self._view.show_alert("Selezionare un numero di artisti valido")
            return
        self._model.percorso(self._current_artist, float(self._view.txtMinDuration.value), int(self._view.txtMaxArtists.value))





