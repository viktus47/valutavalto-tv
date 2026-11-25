
from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

import requests

API_URL = "https://api.frankfurter.app/latest"
DB_NEV = "arfolyam_naplo.db"
DEVIZAK = ("HUF", "EUR", "USD", "GBP", "CHF", "JPY", "CNY", "PLN", "CZK", "CAD", "AUD")

HATTER_SZIN = "#EEF2F6"
FEJLEC_SZIN = "#1E3A8A"
KARTYA_SZIN = "#FFFFFF"
ELSODLEGES_GOMB = "#059669"
TORLES_GOMB = "#DC2626"
KILEPES_GOMB = "#475569"


def tv_atvaltas(osszeg, arfolyam):
    return round(osszeg * arfolyam, 2)


class TvValutaValto:
    def __init__(self, root):
        self.root = root
        self.root.title("Valutaárfolyam-váltó és napló")
        self.root.geometry("740x580")
        self.root.resizable(False, False)
        self.root.configure(bg=HATTER_SZIN)

        self.osszeg_var = tk.StringVar(value="1")
        self.forras_var = tk.StringVar(value="EUR")
        self.cel_var = tk.StringVar(value="HUF")

        self.stilus_beallitas()
        self.adatbazis_letrehozas()
        self.felulet_felepites()
        self.naplo_frissites()

    def stilus_beallitas(self):
        stilus = ttk.Style(self.root)
        stilus.theme_use("clam")

        stilus.configure(
            "TCombobox",
            fieldbackground="#F8FAFC",
            background="#E2E8F0",
            foreground="#0F172A",
            padding=5
        )
        stilus.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#0F172A",
            fieldbackground="#FFFFFF",
            rowheight=26,
            font=("Segoe UI", 10)
        )
        stilus.configure(
            "Treeview.Heading",
            background="#1E293B",
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            padding=6
        )
        stilus.map(
            "Treeview.Heading",
            background=[("active", "#334155")]
        )

    def felulet_felepites(self):
        fejlec = tk.Frame(self.root, bg=FEJLEC_SZIN, pady=14)
        fejlec.pack(fill=tk.X)

        tk.Label(
            fejlec,
            text="Valutaárfolyam-váltó és árfolyamnapló",
            font=("Segoe UI", 16, "bold"),
            bg=FEJLEC_SZIN,
            fg="#FFFFFF"
        ).pack()

        tk.Label(
            fejlec,
            text="Élő devizaárfolyamok és tranzakciós előzmények",
            font=("Segoe UI", 9),
            bg=FEJLEC_SZIN,
            fg="#CBD5E1"
        ).pack(pady=(2, 0))

        fo_keret = tk.Frame(self.root, bg=HATTER_SZIN, padx=20, pady=15)
        fo_keret.pack(fill=tk.BOTH, expand=True)

        kartya = tk.Frame(
            fo_keret,
            bg=KARTYA_SZIN,
            padx=15,
            pady=14,
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )
        kartya.pack(fill=tk.X)

        tk.Label(
            kartya,
            text="Összeg:",
            font=("Segoe UI", 9, "bold"),
            bg=KARTYA_SZIN,
            fg="#334155"
        ).grid(row=0, column=0, sticky=tk.W, padx=5)

        tk.Label(
            kartya,
            text="Erről:",
            font=("Segoe UI", 9, "bold"),
            bg=KARTYA_SZIN,
            fg="#334155"
        ).grid(row=0, column=1, sticky=tk.W, padx=5)

        tk.Label(
            kartya,
            text="Erre:",
            font=("Segoe UI", 9, "bold"),
            bg=KARTYA_SZIN,
            fg="#334155"
        ).grid(row=0, column=3, sticky=tk.W, padx=5)

        osszeg_mezo = tk.Entry(
            kartya,
            textvariable=self.osszeg_var,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            fg="#0F172A",
            relief=tk.SOLID,
            bd=1,
            width=15
        )
        osszeg_mezo.grid(row=1, column=0, padx=5, pady=5, ipady=3)

        forras_valaszto = ttk.Combobox(
            kartya,
            textvariable=self.forras_var,
            values=DEVIZAK,
            state="readonly",
            font=("Segoe UI", 10),
            width=9
        )
        forras_valaszto.grid(row=1, column=1, padx=5, pady=5)

        csere_gomb = tk.Button(
            kartya,
            text="⇄",
            font=("Segoe UI", 11, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            activebackground="#CBD5E1",
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            command=self.deviza_csere
        )
        csere_gomb.grid(row=1, column=2, padx=4, pady=5)

        cel_valaszto = ttk.Combobox(
            kartya,
            textvariable=self.cel_var,
            values=DEVIZAK,
            state="readonly",
            font=("Segoe UI", 10),
            width=9
        )
        cel_valaszto.grid(row=1, column=3, padx=5, pady=5)

        valtas_gomb = tk.Button(
            kartya,
            text="Átváltás és mentés",
            font=("Segoe UI", 10, "bold"),
            bg=ELSODLEGES_GOMB,
            fg="#FFFFFF",
            activebackground="#047857",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=6,
            command=self.atvaltas_esemeny
        )
        valtas_gomb.grid(row=1, column=4, padx=(12, 5), pady=5)

        self.eredmeny_cimke = tk.Label(
            fo_keret,
            text="Eredmény: Válasszon devizapárt és kattintson az átváltásra!",
            font=("Segoe UI", 11, "bold"),
            bg="#DBEAFE",
            fg="#1E3A8A",
            pady=10
        )
        self.eredmeny_cimke.pack(fill=tk.X, pady=12)

        also_sav = tk.Frame(fo_keret, bg=HATTER_SZIN)
        also_sav.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        torles_gomb = tk.Button(
            also_sav,
            text="Napló törlése",
            font=("Segoe UI", 9, "bold"),
            bg=TORLES_GOMB,
            fg="#FFFFFF",
            activebackground="#B91C1C",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=6,
            command=self.naplo_torlese
        )
        torles_gomb.pack(side=tk.LEFT)

        kilepes_gomb = tk.Button(
            also_sav,
            text="Kilépés",
            font=("Segoe UI", 9, "bold"),
            bg=KILEPES_GOMB,
            fg="#FFFFFF",
            activebackground="#334155",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=18,
            pady=6,
            command=self.root.destroy
        )
        kilepes_gomb.pack(side=tk.RIGHT)

        oszlopok = ("idopont", "par", "osszeg", "arfolyam", "eredmeny")
        self.naplo_tabla = ttk.Treeview(
            fo_keret, columns=oszlopok, show="headings", height=7
        )
        self.naplo_tabla.heading("idopont", text="Időpont")
        self.naplo_tabla.heading("par", text="Devizapár")
        self.naplo_tabla.heading("osszeg", text="Összeg")
        self.naplo_tabla.heading("arfolyam", text="Árfolyam")
        self.naplo_tabla.heading("eredmeny", text="Átváltott érték")

        self.naplo_tabla.column("idopont", width=165, anchor=tk.CENTER)
        self.naplo_tabla.column("par", width=115, anchor=tk.CENTER)
        self.naplo_tabla.column("osszeg", width=125, anchor=tk.E)
        self.naplo_tabla.column("arfolyam", width=125, anchor=tk.E)
        self.naplo_tabla.column("eredmeny", width=155, anchor=tk.E)

        self.naplo_tabla.tag_configure("paros", background="#F8FAFC")
        self.naplo_tabla.tag_configure("paratlan", background="#FFFFFF")
        self.naplo_tabla.pack(fill=tk.BOTH, expand=True)

    def deviza_csere(self):
        forras = self.forras_var.get()
        cel = self.cel_var.get()
        self.forras_var.set(cel)
        self.cel_var.set(forras)

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
                f"{eredmeny:.2f} {cel}  (árfolyam: {arfolyam:.4f})"
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

        for index, sor in enumerate(sorok):
            idopont, forras, cel, osszeg, arfolyam, eredmeny = sor
            sor_cimke = "paros" if index % 2 == 0 else "paratlan"
            self.naplo_tabla.insert(
                "",
                tk.END,
                tags=(sor_cimke,),
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