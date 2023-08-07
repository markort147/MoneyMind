# MoneyMind
A simple Python app to manage own finances

## Package Directory Structure

- config/
  - \_\_init\_\_.py
  - config.py
- core/
  - \_\_init\_\_.py
  - transactions.py
- database/
  - \_\_init\_\_.py
  - sqlite_repository.py
- data/ 
  - sqlite_scripts/
    - init.sql 
  - config.yaml
  - sqlite3.db
- logs/ - _will be automatically created when logging is introduced_
- ui/
  - \_\_init\_\_.py
  - command_line.py
- utils/
  - \_\_init\_\_.py
  - pandas_utils.py - _to be created to handle complex queries and visualizations_
- tests/
- main.py
- MoneyMind_win.bat

## to-do list
- logging using the built-in logging module 
- encrypt database using a user-side password
- import and export into CSV
- description column for each transaction field
- split transactions in expenses and earnings - should common fields  share the same database table?
- add credits, debts, loan, interest and scheduled payments - and a feature that predicts future assets trends
- admin mode 
  - to alter database configuration by loading custom scripts at runtime
  - to backup and restore .db file
- use pandas instead of SQL joins/unions for complex queries, in order to have a specific database independent approach
- plots visualization from command line using matplotlib and some graphic library TBD
- finally, an interactive UI - leaving the possibility to switch into command line mode at runtime 