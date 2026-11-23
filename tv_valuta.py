
import tkinter as tk


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

