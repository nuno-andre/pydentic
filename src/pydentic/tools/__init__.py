from .db import Etld


def update_etld_data():
    db = Etld()
    db.create_tables()
    db.populate()
