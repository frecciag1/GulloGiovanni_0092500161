# Sistema Gestionale Spese Personali

Il progetto è stato sviluppato nell'ambito del corso di Fondamenti di informatica, si tratta di un applicativo Python, per la gestione delle spese personali. Il sistema permette di gestire categorie, registrare movimenti, impostare budget mensili e generare report professionali sia a video (come richiesto) che in formato PDF.
I PDF verranno creati in automatico all'interno della cartella src/pdf dopo l'esecuzione dei comandi per i report.

## 1. Requisiti per l’esecuzione

### Compilatore o interprete necessario
* **Python 3.10 o superiore**: È richiesto per il supporto al costrutto `match-case`.

### Librerie utilizzate
Il programma utilizza alcune librerie standard e una libreria esterna per la generazione dei PDF:
1. **Librerie Standard (incluse in Python)**:
   - `sqlite3`: Per la gestione del database relazionale.
   - `datetime`, `os`: Per la gestione di date e file di sistema.
2. **Libreria Esterna (da installare)**:
   - `reportlab`: Necessaria per la creazione dei file PDF professionali.

---

## 2. Installazione e Preparazione

Per eseguire correttamente il programma, occorre aprire il terminale e seguire questi passaggi:

1. **Installazione della libreria per i PDF**:
   ```bash
   pip install reportlab

Avvio del programma:
   python src/main.py
