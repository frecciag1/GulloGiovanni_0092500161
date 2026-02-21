-- Tabella Categorie
CREATE TABLE IF NOT EXISTS Categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE CHECK(length(nome) > 0)
);

-- Tabella Spese
CREATE TABLE IF NOT EXISTS Spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    importo REAL NOT NULL CHECK(importo > 0),
    categoria_id INTEGER NOT NULL,
    descrizione TEXT,
    FOREIGN KEY (categoria_id) REFERENCES Categorie(id)
);

-- Tabella Budget
CREATE TABLE IF NOT EXISTS Budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    importo_limite REAL NOT NULL CHECK(importo_limite > 0),
    UNIQUE(mese, categoria_id),
    FOREIGN KEY (categoria_id) REFERENCES Categorie(id)
);