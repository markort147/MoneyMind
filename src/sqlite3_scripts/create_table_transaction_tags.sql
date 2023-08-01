CREATE TABLE IF NOT EXISTS transaction_tags (
    id_transaction INTEGER,
    id_tag INTEGER,
    PRIMARY KEY (id_transaction, id_tag),
    FOREIGN KEY (id_transaction) REFERENCES transactions(id),
    FOREIGN KEY (id_tag) REFERENCES tags(id)
);