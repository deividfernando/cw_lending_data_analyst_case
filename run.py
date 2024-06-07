import sys
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent
if str(project_dir) not in sys.path:
    sys.path.append(str(project_dir))


from app.orm import init_db
from app.services.populate_database import PopulateDatabase


def run():
    init_db()

    db = PopulateDatabase()

    clients_url = 'https://raw.githubusercontent.com/p-beraldin/lending-data-cases/main/files/clients.csv'
    loans_url = 'https://raw.githubusercontent.com/p-beraldin/lending-data-cases/main/files/loans.csv'

    clients_df = pd.read_csv(clients_url)
    loans_df = pd.read_csv(loans_url)

    db.populate_table('clients', clients_df)
    db.populate_table('loans', loans_df)



