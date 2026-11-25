**Valutaárfolyam-váltó és árfolyamnapló**

**Hallgató:** Tusják Viktor - SRY712

**Feladat leírása:**

Grafikus felületű (Tkinter) valutaárfolyam-váltó alkalmazás, amely az ExchangeRate-API (open.er-api.com) segítségével lekéri az aktuális devizaárfolyamokat, elvégzi az átváltást, és a tranzakciókat egy helyi SQLite adatbázisban ("arfolyam_naplo.db") naplózza és táblázatos formában megjeleníti.

**Indításhoz szükséges modulok:**
- Standard könyvtárak (beépített): "tkinter", "sqlite3", "datetime"
- Külső modul (telepítés: "pip install requests"): "requests"
- Saját modul: "tv_valuta.py"

**Modulok és a modulokban használt függvények**

**1. "requests" (HTTP kéréseket kezelő, bemutatandó modul)**
- "requests.get()" - HTTP GET kérés küldése az árfolyam API végpontjára.
- "valasz.raise_for_status()" - A szerver válaszának HTTP státuszkód ellenőrzése (hibás válasz esetén kivétel dobása).
- "valasz.json()" - A JSON formátumú HTTP válasz feldolgozása Python szótárrá ("dict").

**2. "tkinter" (tanult grafikai modul)**
- "tk.Tk()", "ttk.Frame()", "ttk.Label()", "ttk.Entry()", "ttk.Combobox()", "ttk.Button()", "ttk.Treeview()" - A grafikus felhasználói felület elemeinek létrehozása és elrendezése.
- "messagebox.showwarning()", "messagebox.showerror()", "messagebox.askyesno()" - Felhasználói visszajelzések, hibaüzenetek és megerősítő ablakok kezelése.

**3. "sqlite3" (tanult adatbázis-kezelő modul)**
- "sqlite3.connect()" - Kapcsolódás az SQLite adatbázishoz.
- "kapcsolat.cursor()" - Kurzor objektum létrehozása az SQL utasítások futtatásához.
- "kurzor.execute()" - Tábla létrehozása ("CREATE TABLE"), adatok beszúrása ("INSERT"), lekérdezése ("SELECT") és törlése ("DELETE").
- "kapcsolat.commit()" - Az adatbázis-módosítások véglegesítése.
- "kurzor.fetchall()" - A lekérdezett rekordok listába olvasása.

**4. "datetime" (tanult dátum- és időkezelő modul)**
- "datetime.now()" - Az aktuális rendszeridő lekérdezése.
- "strftime()" - Az időbélyeg szöveges formázása ("ÉÉÉÉ-HH-NN ÓÓ:PP:MM").

**5. "tv_valuta" (saját modul)**
- "tv_atvaltas(osszeg, arfolyam)" - Saját függvény, amely kiszámítja és két tizedesjegyre kerekíti az átváltott összeget.

**Osztály**
- "TvValutaValto" ("tv_valuta.py") - Az alkalmazás grafikus felületét, eseménykezelését, API kommunikációját és SQLite adatbázis műveleteit összefogó fő osztály.