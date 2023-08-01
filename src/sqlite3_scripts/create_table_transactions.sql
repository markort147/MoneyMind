CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description VARCHAR(255) NOT NULL,
    recipient INTEGER,
    date DATE NOT NULL,
    installment INTEGER CHECK (installment IN (0, 1)),
    category INTEGER,
    priority TEXT CHECK (priority IN ('Mandatory', 'Need', 'Voluntary')),
    automatic INTEGER CHECK (automatic IN (0, 1)),
    method INTEGER,
    account INTEGER,
    tags TEXT CHECK (json_valid(tags)),
    FOREIGN KEY (recipient) REFERENCES recipients(id),
    FOREIGN KEY (category) REFERENCES categories(id),
    FOREIGN KEY (method) REFERENCES methods(id),
    FOREIGN KEY (account) REFERENCES accounts(id)
);
