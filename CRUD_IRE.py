"""
Auto noma - SQLite CRUD lietotne (latviski, konsoles izvēlne)

Kā palaist:
1) python auto_noma_app.py
2) Skripts izveidos auto_noma.db (ja tā nav) un tabulas.
3) Izmanto izvēlni CRUD darbībām.
"""

import sqlite3
from sqlite3 import Error

DB_NOSAUKUMS = "mahu_ire.db"


# ---------- DB PALĪGFUNKCIJAS ----------

def iegut_savienojumu():
    """Atver savienojumu ar SQLite DB un ieslēdz ārējās atslēgas (FK)."""
    conn = sqlite3.connect(DB_NOSAUKUMS)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def inicializet_db():
    """Izveido tabulas, ja tās neeksistē."""
    schema_sql = """
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS Klients (
        klients_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        vards_uzvards TEXT NOT NULL,
        telefons     TEXT NOT NULL,
        epasts       TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Auto (
        auto_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        marka        TEXT NOT NULL,
        modelis      TEXT NOT NULL,
        numurzime    TEXT NOT NULL UNIQUE,
        cena_diena   REAL NOT NULL CHECK (cena_diena >= 0),
        statuss      TEXT NOT NULL CHECK (statuss IN ('pieejams', 'iznomats', 'serviss'))
    );

    CREATE TABLE IF NOT EXISTS Ire (
        ire_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        klients_id    INTEGER NOT NULL,
        auto_id       INTEGER NOT NULL,
        sakuma_datums TEXT NOT NULL,  -- YYYY-MM-DD
        beigu_datums  TEXT NOT NULL,  -- YYYY-MM-DD
        kopsumma      REAL NOT NULL CHECK (kopsumma >= 0),
        FOREIGN KEY (klients_id) REFERENCES Klients(klients_id) ON DELETE RESTRICT,
        FOREIGN KEY (auto_id)    REFERENCES Auto(auto_id)       ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS Papildaprikojums (
        papild_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        nosaukums   TEXT NOT NULL UNIQUE,
        cena_diena  REAL NOT NULL CHECK (cena_diena >= 0)
    );

    CREATE TABLE IF NOT EXISTS IrePapild (
        ire_id    INTEGER NOT NULL,
        papild_id INTEGER NOT NULL,
        daudzums  INTEGER NOT NULL CHECK (daudzums > 0),
        PRIMARY KEY (ire_id, papild_id),
        FOREIGN KEY (ire_id)    REFERENCES Ire(ire_id)                 ON DELETE CASCADE,
        FOREIGN KEY (papild_id) REFERENCES Papildaprikojums(papild_id) ON DELETE RESTRICT
    );
    """
    with iegut_savienojumu() as conn:
        conn.executescript(schema_sql)


def izpildit_komandu(sql, parametri=()):
    """Izpilda INSERT/UPDATE/DELETE komandu."""
    try:
        with iegut_savienojumu() as conn:
            cur = conn.cursor()
            cur.execute(sql, parametri)
            conn.commit()
            return cur.lastrowid
    except Error as e:
        print(f"[KĻŪDA] {e}")
        return None


def nolasit_visus(sql, parametri=()):
    """Izpilda SELECT un atgriež sarakstu ar rezultātiem."""
    try:
        with iegut_savienojumu() as conn:
            cur = conn.cursor()
            cur.execute(sql, parametri)
            return cur.fetchall()
    except Error as e:
        print(f"[KĻŪDA] {e}")
        return []


def izdrukat_rindas(virsraksts, rindas):
    """Skaists izvads konsolē."""
    print("\n" + "=" * 70)
    print(virsraksts)
    print("=" * 70)
    if not rindas:
        print("(nav ierakstu)")
    else:
        for r in rindas:
            print(r)


# ---------- CREATE (PIEVIENOT) ----------

def pievienot_klientu():
    vards_uzvards = input("Vārds Uzvārds: ").strip()
    telefons = input("Telefons: ").strip()
    epasts = input("E-pasts (var atstāt tukšu): ").strip() or None

    izpildit_komandu(
        "INSERT INTO Klients(vards_uzvards, telefons, epasts) VALUES (?, ?, ?);",
        (vards_uzvards, telefons, epasts),
    )
    print("✅ Klients pievienots.")


def pievienot_auto():
    marka = input("Marka: ").strip()
    modelis = input("Modelis: ").strip()
    numurzime = input("Numurzīme: ").strip()
    cena_diena = float(input("Cena dienā (EUR): ").strip())
    statuss = input("Statuss (pieejams/iznomats/serviss): ").strip()

    izpildit_komandu(
        "INSERT INTO Auto(marka, modelis, numurzime, cena_diena, statuss) VALUES (?, ?, ?, ?, ?);",
        (marka, modelis, numurzime, cena_diena, statuss),
    )
    print("✅ Auto pievienots.")


def pievienot_papildaprikojumu():
    nosaukums = input("Papildaprīkojuma nosaukums: ").strip()
    cena_diena = float(input("Cena dienā (EUR): ").strip())

    izpildit_komandu(
        "INSERT INTO Papildaprikojums(nosaukums, cena_diena) VALUES (?, ?);",
        (nosaukums, cena_diena),
    )
    print("✅ Papildaprīkojums pievienots.")


def pievienot_iri():
    klients_id = int(input("klients_id: ").strip())
    auto_id = int(input("auto_id: ").strip())
    sakums = input("Sākums (YYYY-MM-DD): ").strip()
    beigas = input("Beigas (YYYY-MM-DD): ").strip()
    kopsumma = float(input("Kopsumma (EUR): ").strip())

    izpildit_komandu(
        "INSERT INTO Ire(klients_id, auto_id, sakuma_datums, beigu_datums, kopsumma) VALUES (?, ?, ?, ?, ?);",
        (klients_id, auto_id, sakums, beigas, kopsumma),
    )
    print("✅ Īre pievienota.")


def pievienot_ires_papildaprikojumu():
    ire_id = int(input("ire_id: ").strip())
    papild_id = int(input("papild_id: ").strip())
    daudzums = int(input("Daudzums: ").strip())

    izpildit_komandu(
        "INSERT INTO IrePapild(ire_id, papild_id, daudzums) VALUES (?, ?, ?);",
        (ire_id, papild_id, daudzums),
    )
    print("✅ Papildaprīkojums piesaistīts īrei.")


# ---------- READ (RĀDĪT) ----------

def radit_klientus():
    rindas = nolasit_visus("SELECT * FROM Klients ORDER BY klients_id;")
    izdrukat_rindas("Klients", rindas)


def radit_auto():
    rindas = nolasit_visus("SELECT * FROM Auto ORDER BY auto_id;")
    izdrukat_rindas("Auto", rindas)


def radit_papildaprikojumus():
    rindas = nolasit_visus("SELECT * FROM Papildaprikojums ORDER BY papild_id;")
    izdrukat_rindas("Papildaprīkojums", rindas)


def radit_ires():
    rindas = nolasit_visus("SELECT * FROM Ire ORDER BY ire_id;")
    izdrukat_rindas("Īre", rindas)


def radit_ires_papildus():
    rindas = nolasit_visus("SELECT * FROM IrePapild ORDER BY ire_id, papild_id;")
    izdrukat_rindas("ĪrePapild", rindas)


def radit_join_skatu():
    """
    JOIN skats: īres + klients + auto + papildaprīkojumu saraksts vienā rindā.
    group_concat saliek vairākus papildaprīkojumus vienā tekstā.
    """
    sql = """
    SELECT
        i.ire_id,
        k.vards_uzvards,
        k.telefons,
        a.marka || ' ' || a.modelis AS auto_nosaukums,
        a.numurzime,
        i.sakuma_datums,
        i.beigu_datums,
        i.kopsumma,
        COALESCE(group_concat(p.nosaukums || ' x' || ip.daudzums, ', '), '-') AS papildaprikojums
    FROM Ire i
    JOIN Klients k ON k.klients_id = i.klients_id
    JOIN Auto a ON a.auto_id = i.auto_id
    LEFT JOIN IrePapild ip ON ip.ire_id = i.ire_id
    LEFT JOIN Papildaprikojums p ON p.papild_id = ip.papild_id
    GROUP BY i.ire_id
    ORDER BY i.ire_id;
    """
    rindas = nolasit_visus(sql)
    izdrukat_rindas("JOIN: Īres + Klients + Auto + Papildaprīkojums", rindas)


# ---------- UPDATE (LABOT) ----------

def labot_klientu():
    klients_id = int(input("Kuram klients_id labot? ").strip())
    vards_uzvards = input("Jauns vārds uzvārds: ").strip()
    telefons = input("Jauns telefons: ").strip()
    epasts = input("Jauns e-pasts (var atstāt tukšu): ").strip() or None

    izpildit_komandu(
        "UPDATE Klients SET vards_uzvards=?, telefons=?, epasts=? WHERE klients_id=?;",
        (vards_uzvards, telefons, epasts, klients_id),
    )
    print("✅ Klients atjaunināts.")


def labot_auto():
    auto_id = int(input("Kuram auto_id labot? ").strip())
    marka = input("Marka: ").strip()
    modelis = input("Modelis: ").strip()
    numurzime = input("Numurzīme: ").strip()
    cena_diena = float(input("Cena dienā: ").strip())
    statuss = input("Statuss (pieejams/iznomats/serviss): ").strip()

    izpildit_komandu(
        "UPDATE Auto SET marka=?, modelis=?, numurzime=?, cena_diena=?, statuss=? WHERE auto_id=?;",
        (marka, modelis, numurzime, cena_diena, statuss, auto_id),
    )
    print("✅ Auto atjaunināts.")


def labot_papildaprikojumu():
    papild_id = int(input("Kuram papild_id labot? ").strip())
    nosaukums = input("Nosaukums: ").strip()
    cena_diena = float(input("Cena dienā: ").strip())

    izpildit_komandu(
        "UPDATE Papildaprikojums SET nosaukums=?, cena_diena=? WHERE papild_id=?;",
        (nosaukums, cena_diena, papild_id),
    )
    print("✅ Papildaprīkojums atjaunināts.")


def labot_iri():
    ire_id = int(input("Kuram ire_id labot? ").strip())
    klients_id = int(input("klients_id: ").strip())
    auto_id = int(input("auto_id: ").strip())
    sakums = input("Sākums (YYYY-MM-DD): ").strip()
    beigas = input("Beigas (YYYY-MM-DD): ").strip()
    kopsumma = float(input("Kopsumma: ").strip())

    izpildit_komandu(
        """UPDATE Ire
           SET klients_id=?, auto_id=?, sakuma_datums=?, beigu_datums=?, kopsumma=?
           WHERE ire_id=?;""",
        (klients_id, auto_id, sakums, beigas, kopsumma, ire_id),
    )
    print("✅ Īre atjaunināta.")


def labot_ires_papildu():
    ire_id = int(input("ire_id: ").strip())
    papild_id = int(input("papild_id: ").strip())
    daudzums = int(input("Jauns daudzums: ").strip())

    izpildit_komandu(
        "UPDATE IrePapild SET daudzums=? WHERE ire_id=? AND papild_id=?;",
        (daudzums, ire_id, papild_id),
    )
    print("✅ ĪrePapild ieraksts atjaunināts.")


# ---------- DELETE (DZĒST) ----------

def dzest_klientu():
    klients_id = int(input("Kuram klients_id dzēst? ").strip())
    izpildit_komandu("DELETE FROM Klients WHERE klients_id=?;", (klients_id,))
    print("🗑️ Klients dzēsts (ja nav saistītu īru).")


def dzest_auto():
    auto_id = int(input("Kuram auto_id dzēst? ").strip())
    izpildit_komandu("DELETE FROM Auto WHERE auto_id=?;", (auto_id,))
    print("🗑️ Auto dzēsts (ja nav saistītu īru).")


def dzest_papildaprikojumu():
    papild_id = int(input("Kuram papild_id dzēst? ").strip())
    izpildit_komandu("DELETE FROM Papildaprikojums WHERE papild_id=?;", (papild_id,))
    print("🗑️ Papildaprīkojums dzēsts (ja nav izmantots īrēs).")


def dzest_iri():
    ire_id = int(input("Kuram ire_id dzēst? ").strip())
    # IrePapild dzēsīsies automātiski (ON DELETE CASCADE)
    izpildit_komandu("DELETE FROM Ire WHERE ire_id=?;", (ire_id,))
    print("🗑️ Īre dzēsta.")


def dzest_ires_papildu():
    ire_id = int(input("ire_id: ").strip())
    papild_id = int(input("papild_id: ").strip())
    izpildit_komandu(
        "DELETE FROM IrePapild WHERE ire_id=? AND papild_id=?;",
        (ire_id, papild_id),
    )
    print("🗑️ ĪrePapild ieraksts dzēsts.")


# ---------- IZVĒLNE ----------

def izvelne():
    print("""
================= AUTO NOMA (CRUD) =================
1)  Pievienot klientu
2)  Pievienot auto
3)  Pievienot papildaprīkojumu
4)  Pievienot īri
5)  Pievienot īres papildaprīkojumu (M:N)

6)  Rādīt klientus
7)  Rādīt auto
8)  Rādīt papildaprīkojumus
9)  Rādīt īres
10) Rādīt IrePapild
11) Rādīt JOIN skatu (īres + viss)

12) Labot klientu
13) Labot auto
14) Labot papildaprīkojumu
15) Labot īri
16) Labot IrePapild

17) Dzēst klientu
18) Dzēst auto
19) Dzēst papildaprīkojumu
20) Dzēst īri
21) Dzēst IrePapild

0)  Iziet
""")


def galvena():
    inicializet_db()

    darbibas = {
        "1": pievienot_klientu,
        "2": pievienot_auto,
        "3": pievienot_papildaprikojumu,
        "4": pievienot_iri,
        "5": pievienot_ires_papildaprikojumu,

        "6": radit_klientus,
        "7": radit_auto,
        "8": radit_papildaprikojumus,
        "9": radit_ires,
        "10": radit_ires_papildus,
        "11": radit_join_skatu,

        "12": labot_klientu,
        "13": labot_auto,
        "14": labot_papildaprikojumu,
        "15": labot_iri,
        "16": labot_ires_papildu,

        "17": dzest_klientu,
        "18": dzest_auto,
        "19": dzest_papildaprikojumu,
        "20": dzest_iri,
        "21": dzest_ires_papildu,
    }

    while True:
        izvelne()
        izvele = input("Izvēle: ").strip()

        if izvele == "0":
            print("Atā!")
            break

        darbiba = darbibas.get(izvele)
        if darbiba:
            darbiba()
        else:
            print("❗ Nepareiza izvēle.")


if __name__ == "__main__":
    galvena()
