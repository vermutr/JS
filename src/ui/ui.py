import copy
from enum import Enum

from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox

from src import data
from src.config.adjacency import Adjacency
from src.config.nodepair import NodePair
from src.data import cities
from src.graph.listGraph import ListGraph
from src.graph.matrixGraph import MatrixGraph
from src.service.bfs import Bfs


class CloseReason(Enum):
    CLOSE = 0,
    OK = 1,
    EDIT = 2


class SetupRoutesForm(object):
    def __init__(self, connection_list=None):
        if connection_list is None:
            connection_list = []

        self.list_of_connections = connection_list
        self.close_reason = CloseReason.CLOSE

        self._window = Tk()
        self._window.title("Connection")
        self._window.resizable(width=False, height=False)

        self._mainframe = ttk.Frame(self._window)
        self._mainframe.grid(column=0, row=0, sticky=(N, W, E, S), padx=5, pady=5)

        Label(self._mainframe, text="City:").grid(row=0, column=0, columnspan=2)

        self._city_a = Combobox(self._mainframe)
        self._city_b = Combobox(self._mainframe)

        self._city_a.grid(row=1, column=0)
        self._city_b.grid(row=1, column=1)

        self._city_a['state'] = 'readonly'
        self._city_b['state'] = 'readonly'

        self._city_a['values'] = sorted(data.cities)
        self._city_b['values'] = sorted(data.cities)

        self._city_a.set(self._city_a['values'][1])
        self._city_b.set(self._city_a['values'][2])

        self._connections_frame = Frame(self._mainframe)
        self._connections_frame.grid(row=2, column=0, columnspan=2)

        self._connection_list = Listbox(self._connections_frame, width=45, listvariable=self.list_of_connections)
        self._connection_list.grid(row=0, column=0, sticky=(W, E))

        self._connection_list_scrollbar = Scrollbar(self._connections_frame, orient=VERTICAL)
        self._connection_list_scrollbar.grid(row=0, column=1, sticky=(N, S))

        self._connection_list.configure(yscrollcommand=self._connection_list_scrollbar.set)
        self._connection_list_scrollbar.config(command=self._connection_list.yview)

        self._connect = Button(self._mainframe, text="Join", command=self.add_connection)
        self._connect.grid(row=3, column=0)

        self._disconnect = Button(self._mainframe, text="Break", command=self.remove_connection)
        self._disconnect.grid(row=3, column=1)

        Label(self._mainframe, text=" ").grid(row=4, column=0, columnspan=2)
        self._confirm = Button(self._mainframe, text="Ok", command=self.confirm_action)
        self._confirm.grid(row=7, column=0, columnspan=2)

        for connection in reversed(self.list_of_connections):
            self._connection_list.insert(0, connection)

    def add_connection(self):
        pair = NodePair(self._city_a.get(), self._city_b.get())
        inverse_pair = NodePair(pair.b, pair.a)

        if pair.a == pair.b:
            messagebox.showwarning("You can not join trace", "You can not join the same city")
            return

        if pair in self.list_of_connections or inverse_pair in self.list_of_connections:
            messagebox.showwarning("You can not join trace", "The cities are already joined")
            return

        self.list_of_connections.insert(0, pair)
        self._connection_list.insert(0, pair)

    def remove_connection(self):
        selected = self._connection_list.curselection()
        if len(selected) != 1:
            return

        self.list_of_connections.pop(selected[0])
        self._connection_list.delete(selected[0])

    def confirm_action(self):
        self.close_reason = CloseReason.OK
        self._window.destroy()

    def show(self):
        self._window.mainloop()


class FindRoutesForm(object):
    def __init__(self, list_of_connections):
        adjacency_lists = Adjacency.adjacency_list(list_of_connections)
        adjacency_matrix = Adjacency.adjacency_matrix(list_of_connections)
        list_based_graph = ListGraph(adjacency_lists)
        matrix_based_graph = MatrixGraph(adjacency_matrix)
        self._list_explorer = Bfs(list_based_graph)
        self._matrix_explorer = Bfs(matrix_based_graph)
        self.close_reason = CloseReason.CLOSE
        self.list_of_connections = list_of_connections

        self._window = Tk()
        self._window.title("Find trace")
        self._window.resizable(width=False, height=False)

        self._mainframe = ttk.Frame(self._window)
        self._mainframe.grid(column=0, row=0, sticky=(N, W, E, S), padx=5, pady=5)

        Label(self._mainframe, text="Start:").grid(row=0, column=0)
        Label(self._mainframe, text="End:").grid(row=0, column=1)

        self._city_from = Combobox(self._mainframe)
        self._city_to = Combobox(self._mainframe)

        self._city_from.grid(row=1, column=0)
        self._city_to.grid(row=1, column=1)

        self._city_from['state'] = 'readonly'
        self._city_to['state'] = 'readonly'

        self._city_from['values'] = sorted(data.cities)
        self._city_to['values'] = sorted(data.cities)

        self._city_from.set(self._city_from['values'][1])
        self._city_to.set(self._city_from['values'][2])

        Label(self._mainframe, text=" ").grid(row=2, column=0, columnspan=2)
        Label(self._mainframe, text="Representation:").grid(row=3, column=0)

        self._representation = Combobox(self._mainframe)
        self._representation.grid(row=3, column=1)
        self._representation['state'] = 'readonly'
        self._representation['values'] = ["Neighborhood Matrix", "Neighborhood lists"]
        self._representation.set(self._representation['values'][0])

        Label(self._mainframe, text=" ").grid(row=4, column=0, columnspan=2)
        self._search = Button(self._mainframe, text="Find", command=self.search)
        self._search.grid(row=5, column=0)

        self._edit = Button(self._mainframe, text="Edit", command=self.edit)
        self._edit.grid(row=5, column=1)

    def search(self):
        explorer = self._matrix_explorer if self._representation.get() == "Neighborhood Matrix" else self._list_explorer
        path = explorer.find_path_cities(self._city_from.get(), self._city_to.get())

        if not path:
            messagebox.showwarning("Trace could not be found", "No trace")
        else:
            temp_list = copy.deepcopy(path)
            path_str = cities[temp_list.pop(0)]
            while len(temp_list) > 0:
                path_str = path_str + " -> " + cities[temp_list.pop(0)]
            messagebox.showinfo("Your trace", path_str)

    def edit(self):
        self.close_reason = CloseReason.EDIT
        self._window.destroy()

    def show(self):
        self._window.mainloop()
