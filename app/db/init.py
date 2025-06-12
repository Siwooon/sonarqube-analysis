# app/db/init_db.py

import sys
from .base import engine, Base
import app.models.user 
import app.models.ressource
import app.models.emprunt

def init_db(drop_first: bool = False):
    """
    Crée toutes les tables SQLAlchemy définies sous Base.
    Si drop_first=True, supprime d'abord toutes les tables existantes.
    """
    if drop_first:
        Base.metadata.drop_all(bind=engine)
        print("Toutes les tables existantes ont été supprimées.")

    Base.metadata.create_all(bind=engine)
    print("Tables créées / mises à jour avec succès.")

if __name__ == "__main__":
    # Exécution : python -m app.db.init_db [--drop]
    drop = "--drop" in sys.argv
    init_db(drop_first=drop)
