-- Creazione della vista "transactions_view"
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
