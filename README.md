# MoneyMind
A simple Python app to manage own finances

# Package Directory Structure

- config/
  - \_\_init\_\_.py
  - config.py
- core/
  - \_\_init\_\_.py
  - transaction.py
  - category.py
  - recipient.py
  - account.py
  - tag.py
  - transaction_repository.py
- database/
  - \_\_init\_\_.py
  - sqlite_repository.py
- data/ 
  - sqlite_scripts/
    - init.sql 
  - config.yaml
  - sqlite3.db
- ui/
  - \_\_init\_\_.py
  - command_line.py
- utils/
  - \_\_init\_\_.py
  - pandas_utils.py
- tests/
- main.py
