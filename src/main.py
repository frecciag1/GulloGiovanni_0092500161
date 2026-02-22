import sqlite3
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def connect_db():
    """
    Stabilisce la connessione con il database SQLite e attiva il supporto alle chiavi esterne.
    
    Returns:
        sqlite3.Connection: Oggetto di connessione al database 'spese_personali.db'.
    """
    conn = sqlite3.connect('spese_personali.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def assicura_cartella_pdf():
    """
    Verifica l'esistenza della cartella src/pdf e la crea se non esiste.
    """
    percorso = os.path.join("src", "pdf")
    if not os.path.exists(percorso):
        os.makedirs(percorso)
    return percorso

def genera_pdf(nome_file, titolo, intestazioni, dati):
    """
    Funzione di utilità per creare un file PDF ben formattato.
    
    Args:
        nome_file (str): Nome del file (es. report1.pdf).
        titolo (str): Titolo del report all'interno del documento.
        intestazioni (list): Lista delle intestazioni della tabella.
        dati (list): Lista di tuple contenenti i record del database.
    """
    cartella = assicura_cartella_pdf()
    percorso_completo = os.path.join(cartella, nome_file)
    
    doc = SimpleDocTemplate(percorso_completo, pagesize=letter)
    elementi = []
    stili = getSampleStyleSheet()
    
    # Aggiunta Titolo
    elementi.append(Paragraph(titolo, stili['Title']))
    elementi.append(Spacer(1, 12))
    
    # Preparazione Tabella
    tabella_dati = [intestazioni] + dati
    t = Table(tabella_dati)
    
    # Stile Tabella
    stile_tabella = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    t.setStyle(stile_tabella)
    
    elementi.append(t)
    doc.build(elementi)
    print(f"File PDF creato con successo: {percorso_completo}")

def menu_principale():
    """Visualizza il menu principale e acquisisce la scelta."""
    print("\n----------------------------------")
    print("     SISTEMA SPESE PERSONALI      ")
    print("----------------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report (Console + PDF)")
    print("5. Esci")
    print("----------------------------------")
    return input("Inserisci la tua scelta: ")

def gestione_categorie(conn):
    """Gestisce l'inserimento di una nuova categoria."""
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

def inserisci_spesa(conn):
    """Registra una nuova spesa nel DB."""
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
        cursor.execute("INSERT INTO Spese (data, importo, categoria_id, descrizione) VALUES (?, ?, ?, ?)", 
                       (data, importo, res[0], desc))
        conn.commit()
        print("Spesa inserita correttamente.")
    else:
        print("Errore: la categoria non esiste.")

def definisci_budget(conn):
    """Imposta o aggiorna il budget mensile per una categoria."""
    mese = input("Mese (YYYY-MM): ")
    nome_cat = input("Nome della categoria: ")
    try:
        importo = float(input("Importo del budget: "))
    except ValueError:
        print("Errore: Inserire un numero valido.")
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Categorie WHERE nome = ?", (nome_cat,))
    res = cursor.fetchone()
    if res:
        cursor.execute("""
            INSERT INTO Budget (mese, categoria_id, importo_limite) VALUES (?, ?, ?)
            ON CONFLICT(mese, categoria_id) DO UPDATE SET importo_limite=excluded.importo_limite
        """, (mese, res[0], importo))
        conn.commit()
        print("Budget salvato.")
    else:
        print("Errore categoria.")

def visualizza_report(conn):
    """
    Gestisce il sotto-menù della reportistica.
    Visualizza i dati formattati in console e genera contemporaneamente i file PDF.
    Resta all'interno di questo menù finché l'utente non sceglie di uscire con l'opzione 4.

    Args:
        conn (sqlite3.Connection): Connessione attiva al database.
    """
    while True:
        print("\n--- MENU REPORT ---")
        print("1. Totale spese per categoria (Console + PDF: report1.pdf)")
        print("2. Spese mensili vs budget (Console + PDF: report2.pdf)")
        print("3. Elenco completo spese (Console + PDF: report3.pdf)")
        print("4. Ritorna al menu principale")
        
        scelta_rep = input("Inserisci scelta: ")
        cursor = conn.cursor()

        match scelta_rep:
            case "1":
                cursor.execute("""
                    SELECT c.nome, SUM(s.importo) 
                    FROM Spese s 
                    JOIN Categorie c ON s.categoria_id = c.id 
                    GROUP BY c.nome
                """)
                risultati = cursor.fetchall()
                if risultati:
                    # Visualizzazione a video
                    print(f"\n{'CATEGORIA':<20} | {'TOTALE SPESO':<12}")
                    print("-" * 35)
                    for r in risultati:
                        print(f"{r[0]:<20} | € {r[1]:>10.2f}")
                    
                    # Generazione PDF
                    dati_pdf = [(r[0], f"{r[1]:.2f}") for r in risultati]
                    genera_pdf("report1.pdf", "Totale Spese per Categoria", ["Categoria", "Totale (€)"], dati_pdf)
                else:
                    print("Nessun dato disponibile.")
            
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
                risultati = cursor.fetchall()
                if risultati:
                    # Visualizzazione a video
                    print(f"\n{'CATEGORIA':<15} | {'BUDGET':<10} | {'SPESO':<10} | {'STATO'}")
                    print("-" * 55)
                    for r in risultati:
                        stato = "OK" if r[2] <= r[1] else "!! OVER !!"
                        print(f"{r[0]:<15} | € {r[1]:>8.2f} | € {r[2]:>8.2f} | {stato}")
                    
                    # Generazione PDF
                    dati_pdf = [(r[0], f"{r[1]:.2f}", f"{r[2]:.2f}", "OK" if r[2] <= r[1] else "OVER") for r in risultati]
                    genera_pdf("report2.pdf", f"Analisi Budget Mese: {mese}", ["Categoria", "Budget", "Speso", "Stato"], dati_pdf)
                else:
                    print(f"Nessun budget definito per il mese {mese}.")

            case "3":
                cursor.execute("""
                    SELECT s.data, c.nome, s.importo, s.descrizione 
                    FROM Spese s 
                    JOIN Categorie c ON s.categoria_id = c.id 
                    ORDER BY s.data ASC
                """)
                risultati = cursor.fetchall()
                if risultati:
                    # Visualizzazione a video
                    print(f"\n{'DATA':<12} | {'CATEGORIA':<15} | {'IMPORTO':<10} | {'DESCRIZIONE'}")
                    print("-" * 65)
                    for r in risultati:
                        desc = r[3] if r[3] else "-"
                        print(f"{r[0]:<12} | {r[1]:<15} | € {r[2]:>8.2f} | {desc}")
                    
                    # Generazione PDF
                    dati_pdf = [(r[0], r[1], f"{r[2]:.2f}", r[3]) for r in risultati]
                    genera_pdf("report3.pdf", "Elenco Completo Spese", ["Data", "Categoria", "Importo", "Note"], dati_pdf)
                else:
                    print("Nessuna spesa registrata.")

            case "4":
                print("Ritorno al menù principale...")
                break
            
            case _:
                print("Scelta non valida. Riprovare.")


def popola_dati_esempio(conn):
    """Dati demo per la presentazione."""
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Categorie (nome) VALUES ('Alimentari')")
    cursor.execute("INSERT OR IGNORE INTO Categorie (nome) VALUES ('Trasporti')")
    conn.commit()

def main():
    """Main entry point."""
    conn = connect_db()
    try:
        with open('sql/database.sql', 'r') as f:
            conn.executescript(f.read())
        popola_dati_esempio(conn)
    except FileNotFoundError:
        print("Errore caricamento SQL.")
    
    while True:
        scelta = menu_principale()
        match scelta:
            case "1": gestione_categorie(conn)
            case "2": inserisci_spesa(conn)
            case "3": definisci_budget(conn)
            case "4": visualizza_report(conn)
            case "5": break
    conn.close()

if __name__ == "__main__":
    main()