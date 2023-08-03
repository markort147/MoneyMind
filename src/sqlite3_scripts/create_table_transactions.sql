CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    description VARCHAR(255) NOT NULL,
    recipient INTEGER NOT NULL,
    date DATE NOT NULL,
    installment INTEGER CHECK (installment IN (0, 1)),
    category INTEGER NOT NULL,
    priority TEXT CHECK (priority IN ('Mandatory', 'Need', 'Voluntary')),
    automatic INTEGER CHECK (automatic IN (0, 1)),
    method INTEGER NOT NULL,
    account INTEGER NOT NULL,
    tags VARCHAR(255),
    FOREIGN KEY (recipient) REFERENCES recipients(id),
    FOREIGN KEY (category) REFERENCES categories(id),
    FOREIGN KEY (method) REFERENCES methods(id),
    FOREIGN KEY (account) REFERENCES accounts(id)
);
