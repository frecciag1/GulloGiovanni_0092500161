import sqlite3
from datetime import datetime

def connect_db():
    # Connessione al database e attivazione dei vincoli di chiave esterna
    conn = sqlite3.connect('spese_personali.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def menu_principale():
    print("\n----------------------------------")
    print("     SISTEMA SPESE PERSONALI      ")
    print("----------------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("----------------------------------")
    return input("Inserisci la tua scelta: ")

# MODULO 1: Gestione Categorie
def gestione_categorie(conn):
    nome = input("Nome della categoria: ").strip()
    if not nome:
        print("Errore: Il nome non può essere vuoto.")
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Categorie (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")
    except sqlite3.IntegrityError:
        print("Errore: La categoria esiste già.")

# MODULO 2: Inserimento di una Spesa
def inserisci_spesa(conn):
    data = input("Data (YYYY-MM-DD): ")
    try:
        importo = float(input("Importo: "))
        if importo <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: Inserire un numero valido.")
        return

    cat_nome = input("Nome categoria: ")
    desc = input("Descrizione (facoltativa): ")

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Categorie WHERE nome = ?", (cat_nome,))
    res = cursor.fetchone()
    
    if res:
        try:
            cursor.execute("INSERT INTO Spese (data, importo, categoria_id, descrizione) VALUES (?, ?, ?, ?)", 
                           (data, importo, res[0], desc))
            conn.commit()
            print("Spesa inserita correttamente.")
        except sqlite3.Error as e:
            print(f"Errore durante l'inserimento: {e}")
    else:
        print("Errore: la categoria non esiste.")

# MODULO 3: Definizione del Budget Mensile
def definisci_budget(conn):
    mese = input("Mese (YYYY-MM): ")
    nome_cat = input("Nome della categoria: ")
    try:
        importo = float(input("Importo del budget: "))
        if importo <= 0:
            print("Errore: il budget deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: Inserire un numero valido.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Categorie WHERE nome = ?", (nome_cat,))
    res = cursor.fetchone()

    if res:
        try:
            # Inserisce o aggiorna se esiste già un budget per quel mese/categoria
            cursor.execute("""
                INSERT INTO Budget (mese, categoria_id, importo_limite) VALUES (?, ?, ?)
                ON CONFLICT(mese, categoria_id) DO UPDATE SET importo_limite=excluded.importo_limite
            """, (mese, res[0], importo))
            conn.commit()
            print("Budget mensile salvato correttamente.")
        except sqlite3.Error as e:
            print(f"Errore database: {e}")
    else:
        print("Errore: la categoria non esiste.")

# MODULO 4: Visualizzazione dei Report
def visualizza_report(conn):
    print("\n--- MENU REPORT ---")
    print("1. Totale spese per categoria")
    print("2. Spese mensili vs budget")
    print("3. Elenco completo delle spese ordinate per data")
    print("4. Ritorna al menu principale")
    
    scelta_rep = input("Inserisci scelta: ")
    cursor = conn.cursor()

    match scelta_rep:
        case "1":
            cursor.execute("""
                SELECT c.nome, SUM(s.importo) FROM Spese s 
                JOIN Categorie c ON s.categoria_id = c.id GROUP BY c.nome
            """)
            print("\nCategoria | Totale Speso")
            for r in cursor.fetchall():
                print(f"{r[0]} | {r[1]:.2f}")
        
        case "2":
            mese = input("Inserisci mese (YYYY-MM): ")
            cursor.execute("""
                SELECT c.nome, b.importo_limite, IFNULL(SUM(s.importo), 0)
                FROM Budget b
                JOIN Categorie c ON b.categoria_id = c.id
                LEFT JOIN Spese s ON c.id = s.categoria_id AND strftime('%Y-%m', s.data) = b.mese
                WHERE b.mese = ?
                GROUP BY c.nome
            """, (mese,))
            results = cursor.fetchall()
            if not results:
                print("Nessun budget definito per questo mese.")
            else:
                for r in results:
                    stato = "OK" if r[2] <= r[1] else "SUPERAMENTO BUDGET"
                    print(f"Mese: {mese}\nCategoria: {r[0]}\nBudget: {r[1]:.2f}\nSpeso: {r[2]:.2f}\nStato: {stato}\n")

        case "3":
            cursor.execute("""
                SELECT s.data, c.nome, s.importo, s.descrizione 
                FROM Spese s JOIN Categorie c ON s.categoria_id = c.id 
                ORDER BY s.data ASC
            """)
            print("\nData | Categoria | Importo | Descrizione")
            for r in cursor.fetchall():
                print(f"{r[0]} | {r[1]} | {r[2]:.2f} | {r[3]}")
        
        case "4":
            return
        
        case _:
            print("Scelta non valida.")

# FUNZIONE DI SUPPORTO: Dati di esempio per la dimostrazione
def popola_dati_esempio(conn):
    cursor = conn.cursor()
    # Inserimento Categorie
    categorie = [('Alimentari',), ('Trasporti',), ('Svago',)]
    cursor.executemany("INSERT OR IGNORE INTO Categorie (nome) VALUES (?)", categorie)
    
    # Inserimento Budget per dimostrare il confronto (Report 2)
    budget = [('2025-01', 1, 300.00), ('2025-01', 2, 100.00)]
    cursor.executemany("INSERT OR IGNORE INTO Budget (mese, categoria_id, importo_limite) VALUES (?, ?, ?)", budget)
    
    # Inserimento Spese per dimostrare i report
    spese = [
        ('2025-01-10', 50.50, 1, 'Spesa supermercato'),
        ('2025-01-15', 270.00, 1, 'Cena ristorante'), # Supera budget Alimentari
        ('2025-01-12', 20.00, 2, 'Benzina')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Spese (data, importo, categoria_id, descrizione) VALUES (?, ?, ?, ?)", spese)
    conn.commit()

def main():
    print("Avvio del Sistema Gestionale Spese...")
    conn = connect_db()
    
    # Inizializzazione Tabelle da file SQL
    try:
        with open('sql/database.sql', 'r') as f:
            conn.executescript(f.read())
        # Carica dati iniziali per la demo
        popola_dati_esempio(conn)
    except FileNotFoundError:
        print("Errore: file sql/database.sql non trovato. Assicurarsi che la struttura delle cartelle sia corretta.")
        return

    while True:
        scelta = menu_principale()
        
        match scelta:
            case "1":
                gestione_categorie(conn)
            case "2":
                inserisci_spesa(conn)
            case "3":
                definisci_budget(conn)
            case "4":
                visualizza_report(conn)
            case "5":
                print("Chiusura del programma. Arrivederci!")
                break
            case _:
                print("Scelta non valida. Riprovare.")
                
    conn.close()

if __name__ == "__main__":
    main()