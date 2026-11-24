
from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

import requests

API_URL = "https://api.frankfurter.app/latest"
DB_NEV = "arfolyam_naplo.db"
DEVIZAK = ("HUF", "EUR", "USD", "GBP", "CHF", "JPY", "CNY", "PLN", "CZK", "CAD", "AUD")


def tv_atvaltas(osszeg, arfolyam):
    return round(osszeg * arfolyam, 2)


class TvValutaValto:
    def __init__(self, root):
        self.root = root
        self.root.title("Valutaárfolyam-váltó és napló")
        self.root.geometry("680x460")
        self.root.resizable(False, False)

        self.osszeg_var = tk.StringVar(value="1")
        self.forras_var = tk.StringVar(value="EUR")
        self.cel_var = tk.StringVar(value="HUF")

        self.adatbazis_letrehozas()
        self.felulet_felepites()
        self.naplo_frissites()

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
            text="Átváltás és mentés",
            command=self.atvaltas_esemeny
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
            text="Napló törlése",
            command=self.naplo_torlese
        )
        torles_gomb.grid(row=5, column=0, sticky=tk.W, padx=5)

        kilepes_gomb = ttk.Button(
            fo_keret,
            text="Kilépés",
            command=self.root.destroy
        )
        kilepes_gomb.grid(row=5, column=3, sticky=tk.E, padx=5)

    def adatbazis_letrehozas(self):
        with sqlite3.connect(DB_NEV) as kapcsolat:
            kurzor = kapcsolat.cursor()
            kurzor.execute(
                """
                CREATE TABLE IF NOT EXISTS atvaltasok (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    idopont TEXT NOT NULL,
                    forras TEXT NOT NULL,
                    cel TEXT NOT NULL,
                    osszeg REAL NOT NULL,
                    arfolyam REAL NOT NULL,
                    eredmeny REAL NOT NULL
                )
                """
            )
            kapcsolat.commit()

    def arfolyam_lekeres(self, forras, cel):
        if forras == cel:
            return 1.0

        parameterek = {"from": forras, "to": cel}
        valasz = requests.get(API_URL, params=parameterek, timeout=5)
        valasz.raise_for_status()
        adatok = valasz.json()
        return float(adatok["rates"][cel])

    def atvaltas_esemeny(self):
        try:
            nyers_szoveg = self.osszeg_var.get().replace(",", ".")
            osszeg = float(nyers_szoveg)
            if osszeg <= 0:
                messagebox.showwarning(
                    "Hibás adat", "Pozitív összeget adjon meg!"
                )
                return
        except ValueError:
            messagebox.showerror(
                "Hibás adat", "Érvényes számot adjon meg!"
            )
            return

        forras = self.forras_var.get()
        cel = self.cel_var.get()

        try:
            arfolyam = self.arfolyam_lekeres(forras, cel)
        except requests.RequestException as hiba:
            messagebox.showerror(
                "Hálózati hiba",
                f"Nem sikerült lekérni az árfolyamot:\n{hiba}"
            )
            return

        eredmeny = tv_atvaltas(osszeg, arfolyam)
        self.eredmeny_cimke.configure(
            text=(
                f"Eredmény: {osszeg:.2f} {forras} = "
                f"{eredmeny:.2f} {cel} (árfolyam: {arfolyam:.4f})"
            )
        )
        self.mentes_adatbazisba(forras, cel, osszeg, arfolyam, eredmeny)
        self.naplo_frissites()

    def mentes_adatbazisba(
        self, forras, cel, osszeg, arfolyam, eredmeny
    ):
        idopont = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(DB_NEV) as kapcsolat:
            kurzor = kapcsolat.cursor()
            kurzor.execute(
                """
                INSERT INTO atvaltasok
                (idopont, forras, cel, osszeg, arfolyam, eredmeny)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (idopont, forras, cel, osszeg, arfolyam, eredmeny)
            )
            kapcsolat.commit()

    def naplo_frissites(self):
        for elem in self.naplo_tabla.get_children():
            self.naplo_tabla.delete(elem)

        with sqlite3.connect(DB_NEV) as kapcsolat:
            kurzor = kapcsolat.cursor()
            kurzor.execute(
                """
                SELECT idopont, forras, cel, osszeg, arfolyam, eredmeny
                FROM atvaltasok
                ORDER BY id DESC
                """
            )
            sorok = kurzor.fetchall()

        for sor in sorok:
            idopont, forras, cel, osszeg, arfolyam, eredmeny = sor
            self.naplo_tabla.insert(
                "",
                tk.END,
                values=(
                    idopont,
                    f"{forras} -> {cel}",
                    f"{osszeg:.2f}",
                    f"{arfolyam:.4f}",
                    f"{eredmeny:.2f}"
                )
            )

    def naplo_torlese(self):
        megerosites = messagebox.askyesno(
            "Megerősítés",
            "Biztosan törli a teljes árfolyamnaplót?"
        )
        if not megerosites:
            return

        with sqlite3.connect(DB_NEV) as kapcsolat:
            kurzor = kapcsolat.cursor()
            kurzor.execute("DELETE FROM atvaltasok")
            kapcsolat.commit()

        self.naplo_frissites()