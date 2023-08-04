CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method_name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS recipients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_name VARCHAR(255) NOT NULL--,
    --recipient_type VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS transaction_tags (
    id_transaction INTEGER,
    id_tag INTEGER,
    PRIMARY KEY (id_transaction, id_tag),
    FOREIGN KEY (id_transaction) REFERENCES transactions(id),
    FOREIGN KEY (id_tag) REFERENCES tags(id)
);
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
CREATE VIEW IF NOT EXISTS transactions_view  AS
SELECT
    t.id AS transaction_id,
    t.amount,
    t.description,
    r.recipient_name,
    --r.recipient_type,
    t.date,
    t.installment,
    c.category_name,
    t.priority,
    t.automatic,
    m.method_name,
    a.account_name,
    GROUP_CONCAT(tg.tag_name, ', ') AS tags
FROM transactions t
LEFT JOIN recipients r ON t.recipient = r.id
LEFT JOIN categories c ON t.category = c.id
LEFT JOIN methods m ON t.method = m.id
LEFT JOIN accounts a ON t.account = a.id
LEFT JOIN transaction_tags tt ON t.id = tt.id_transaction
LEFT JOIN tags tg ON tt.id_tag = tg.id
GROUP BY t.id;
