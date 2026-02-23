import sqlite3

def inizializza_database():
    # Crea la connessione (crea il file se non esiste)
    conn = sqlite3.connect('spese_personali.db')
    cursor = conn.cursor()
    
    # Carica lo script SQL dal file esterno [cite: 130, 188]
    try:
        with open('sql/database.sql', 'r') as file_sql:
            script_sql = file_sql.read()
            # Esegue tutte le istruzioni CREATE TABLE [cite: 132]
            cursor.executescript(script_sql)
            conn.commit()
    except FileNotFoundError:
        print("Errore: file database.sql non trovato nella cartella sql/")
    
    return conn