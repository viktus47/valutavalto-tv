import tkinter as tk
from tkinter import ttk

DEVIZAK = ("HUF", "EUR", "USD", "GBP", "CHF")


class TvValutaValto:
    def __init__(self, root):
        self.root = root
        self.root.title("Valutaárfolyam-váltó és napló")
        self.root.geometry("680x460")
        self.root.resizable(False, False)

        self.osszeg_var = tk.StringVar(value="100")
        self.forras_var = tk.StringVar(value="EUR")
        self.cel_var = tk.StringVar(value="HUF")

        self.felulet_felepites()

    def felulet_felepites(self):
        fo_keret = ttk.Frame(self.root, padding=15)
        fo_keret.pack(fill=tk.BOTH, expand=True)

        cim = ttk.Label(
            fo_keret,
            text="Valutaárfolyam-váltó és árfolyamnapló",
            font=("Arial", 14, "bold")
        )
        cim.grid(row=0, column=0, columnspan=4, pady=(0, 15))

        ttk.Label(fo_keret, text="Összeg:").grid(
            row=1, column=0, sticky=tk.W, padx=5
        )
        ttk.Label(fo_keret, text="Erről:").grid(
            row=1, column=1, sticky=tk.W, padx=5
        )
        ttk.Label(fo_keret, text="Erre:").grid(
            row=1, column=2, sticky=tk.W, padx=5
        )

        osszeg_mezo = ttk.Entry(
            fo_keret, textvariable=self.osszeg_var, width=16
        )
        osszeg_mezo.grid(row=2, column=0, padx=5, pady=5)

        forras_valaszto = ttk.Combobox(
            fo_keret,
            textvariable=self.forras_var,
            values=DEVIZAK,
            state="readonly",
            width=10
        )
        forras_valaszto.grid(row=2, column=1, padx=5, pady=5)

        cel_valaszto = ttk.Combobox(
            fo_keret,
            textvariable=self.cel_var,
            values=DEVIZAK,
            state="readonly",
            width=10
        )
        cel_valaszto.grid(row=2, column=2, padx=5, pady=5)

        valtas_gomb = ttk.Button(
            fo_keret,
            text="Átváltás és mentés"
        )
        valtas_gomb.grid(row=2, column=3, padx=5, pady=5)

        self.eredmeny_cimke = ttk.Label(
            fo_keret,
            text="Eredmény: -",
            font=("Arial", 11, "bold")
        )
        self.eredmeny_cimke.grid(
            row=3, column=0, columnspan=4, pady=15
        )

        oszlopok = ("idopont", "par", "osszeg", "arfolyam", "eredmeny")
        self.naplo_tabla = ttk.Treeview(
            fo_keret, columns=oszlopok, show="headings", height=10
        )
        self.naplo_tabla.heading("idopont", text="Időpont")
        self.naplo_tabla.heading("par", text="Devizapár")
        self.naplo_tabla.heading("osszeg", text="Összeg")
        self.naplo_tabla.heading("arfolyam", text="Árfolyam")
        self.naplo_tabla.heading("eredmeny", text="Átváltott érték")

        self.naplo_tabla.column("idopont", width=150, anchor=tk.CENTER)
        self.naplo_tabla.column("par", width=100, anchor=tk.CENTER)
        self.naplo_tabla.column("osszeg", width=110, anchor=tk.E)
        self.naplo_tabla.column("arfolyam", width=110, anchor=tk.E)
        self.naplo_tabla.column("eredmeny", width=130, anchor=tk.E)

        self.naplo_tabla.grid(
            row=4, column=0, columnspan=4, pady=(0, 10)
        )

        torles_gomb = ttk.Button(
            fo_keret,
            text="Napló törlése"
        )
        torles_gomb.grid(row=5, column=0, sticky=tk.W, padx=5)

        kilepes_gomb = ttk.Button(
            fo_keret,
            text="Kilépés"
        )
        kilepes_gomb.grid(row=5, column=3, sticky=tk.E, padx=5)