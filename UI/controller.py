import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.chosen_business1 = None
        self.chosen_business2 = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_city(self):
        for city in self.model.cities:
            self.view.dd_city.options.append(ft.dropdown.Option(city))

    def handle_crea_grafo(self, e):
        if self.view.dd_city.value is None:
            self.view.create_alert("Selezionare una città")
            return
        city = self.view.dd_city.value
        self.model.build_graph(city)
        self.fill_dd_locali()
        self.view.txt_result.controls.clear()
        nodi, archi = self.model.get_graph_details()
        self.view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nodi} nodi e {archi} archi"))
        self.view.update_page()

    def fill_dd_locali(self):
        for business in self.model.graph.nodes:
            self.view.dd_locale1.options.append(ft.dropdown.Option(data=business,
                                                                   text=business,
                                                                   on_click=self.choose_business1))
            self.view.dd_locale2.options.append(ft.dropdown.Option(data=business,
                                                                   text=business,
                                                                   on_click=self.choose_business2))

    def choose_business1(self, e):
        if e.control.data is None:
            self.chosen_business1 = None
        self.chosen_business1 = e.control.data

    def choose_business2(self, e):
        if e.control.data is None:
            self.chosen_business2 = None
        self.chosen_business2 = e.control.data

    def handle_locale_distante(self, e):
        if self.chosen_business1 is None:
            self.view.create_alert("Selezionare un locale L1")
            return
        locale, distanza = self.model.get_farthest_node(self.chosen_business1)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il locale più distante da {self.chosen_business1} è {locale}, "
                                                     f"{distanza} km"))
        self.view.update_page()

    def handle_percorso(self, e):
        if self.chosen_business1 is None or self.chosen_business2 is None:
            self.view.create_alert("Selezionare due locali L1 e L2")
            return
        try:
            soglia = int(self.view.txt_soglia.value)
        except ValueError:
            self.view.create_alert("Inserire un numero")
            return
        path, km = self.model.get_percorso(self.chosen_business1, self.chosen_business2, soglia)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il percorso con più locali da {self.chosen_business1} a "
                                                     f"{self.chosen_business2} è il seguente:"))
        for p in path:
            self.view.txt_result.controls.append(ft.Text(p))
        self.view.txt_result.controls.append(ft.Text(f"In tutto sono stati percorsi {km} km"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
