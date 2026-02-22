# Sistema Gestionale Spese Personali

Il progetto implementato è un applicativo Python per la gestione delle spese personali, sviluppato come elaborato per il corso di Fondamenti di informatica. 
Il sistema permette di gestire categorie, registrare spese, impostare budget mensili e visualizzare report dettagliati, utilizzando SQLite per la persistenza dei dati.

## 1. Requisiti per l’esecuzione

### Compilatore o interprete necessario
* **Python 3.10 o superiore**: È necessario l'interprete Python in una versione recente (3.10+) per supportare il costrutto `match-case` (lo switch di Python) utilizzato nel codice.

### Eventuali librerie standard utilizzate
Il programma utilizza esclusivamente librerie standard di Python, pertanto non è necessaria l'installazione di pacchetti esterni tramite `pip`.
* `sqlite3`: Per la gestione del database relazionale.
* `datetime`: Per la gestione e la formattazione delle date.
* `os`: Per la gestione dei percorsi dei file di sistema.

---

## 2. Istruzioni dettagliate per eseguire il programma

### Istruzioni di compilazione
Essendo un linguaggio interpretato, **Python non richiede una fase di compilazione** preventiva. Il codice sorgente viene eseguito direttamente dall'interprete.

### Istruzioni di avvio del programma
1. Assicurarsi che la struttura delle cartelle sia la seguente:
   - `main.py` (nella cartella `src/` o nella root)
   - `sql/database.sql` (contiene lo script di creazione delle tabelle)
2. Aprire il terminale o il prompt dei comandi nella cartella principale del progetto.

### Comando esatto da eseguire
Dalla cartella principale, eseguire il seguente comando:

```bash
python src/main.py
