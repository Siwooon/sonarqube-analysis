# scripts/load_fixtures.py

import uuid
import sys

from app.db.base import Base, engine, SessionLocal
from app.models.user import User
from app.models.ressource import Ressource
from app.models.emprunt import Emprunt


def main(drop_first: bool = True):
    """
    Initialise et charge les fixtures dans la base de données.
    Si drop_first=True, supprime d'abord toutes les tables existantes.
    """
    if drop_first:
        Base.metadata.drop_all(bind=engine)
        print("→ Tables existantes supprimées")
    Base.metadata.create_all(bind=engine)
    print("→ Tables (re)créées")

    db = SessionLocal()
    try:
        # 1. DÉCLARATION DES DONNÉES
        users_data = [
            {"nom": "Dupont", "prenom": "Jean", "mail": "jean.dupont@mail.com", "numero_telephone": "+33601020304", "nationalite": "Française"},
            {"nom": "Martin", "prenom": "Alice", "mail": "alice.martin@mail.com", "numero_telephone": "+32477112233", "nationalite": "Belge"},
            {"nom": "Garcia", "prenom": "Pablo", "mail": "pablo.garcia@mail.com", "numero_telephone": "+34911223344", "nationalite": "Espagnole"},
            {"nom": "Smith", "prenom": "Emily", "mail": "emily.smith@mail.com", "numero_telephone": "+447700900123", "nationalite": "Anglaise"},
            {"nom": "Nguyen", "prenom": "Minh", "mail": "minh.nguyen@mail.com", "numero_telephone": "+84912345678", "nationalite": "Vietnamienne"},
            {"nom": "Kowalski", "prenom": "Anna", "mail": "anna.kowalski@mail.com", "numero_telephone": "+48221122334", "nationalite": "Polonaise"},
            {"nom": "Dubois", "prenom": "Lucas", "mail": "lucas.dubois@mail.com", "numero_telephone": "+33698765432", "nationalite": "Française"},
            {"nom": "Schmidt", "prenom": "Sophie", "mail": "sophie.schmidt@mail.com", "numero_telephone": "+4915112345678", "nationalite": "Allemande"},
            {"nom": "Rossi", "prenom": "Marco", "mail": "marco.rossi@mail.com", "numero_telephone": "+393491234567", "nationalite": "Italienne"},
            {"nom": "Fernandez", "prenom": "Lucia", "mail": "lucia.fernandez@mail.com", "numero_telephone": "+34611223344", "nationalite": "Espagnole"}
        ]

        livres_data = [
            {"titre": "1984", "auteur": "George Orwell"},
            {"titre": "Le Seigneur des Anneaux", "auteur": "J.R.R. Tolkien"},
            {"titre": "Harry Potter à l'école des sorciers", "auteur": "J.K. Rowling"},
            {"titre": "Fahrenheit 451", "auteur": "Ray Bradbury"},
            {"titre": "Le Petit Prince", "auteur": "Antoine de Saint-Exupéry"},
            {"titre": "L'Étranger", "auteur": "Albert Camus"},
            {"titre": "Les Misérables", "auteur": "Victor Hugo"},
            {"titre": "La Peste", "auteur": "Albert Camus"},
            {"titre": "Le Comte de Monte-Cristo", "auteur": "Alexandre Dumas"},
            {"titre": "Orgueil et Préjugés", "auteur": "Jane Austen"}
        ]

        films_data = [
            {"titre": "Inception", "auteur": "Christopher Nolan"},
            {"titre": "Le Parrain", "auteur": "Francis Ford Coppola"},
            {"titre": "Pulp Fiction", "auteur": "Quentin Tarantino"},
            {"titre": "Interstellar", "auteur": "Christopher Nolan"},
            {"titre": "Forrest Gump", "auteur": "Robert Zemeckis"},
            {"titre": "La Liste de Schindler", "auteur": "Steven Spielberg"},
            {"titre": "Fight Club", "auteur": "David Fincher"},
            {"titre": "Le Fabuleux Destin d'Amélie Poulain", "auteur": "Jean-Pierre Jeunet"},
            {"titre": "Matrix", "auteur": "Les Wachowski"},
            {"titre": "Parasite", "auteur": "Bong Joon-ho"}
        ]

        jeux_data = [
            {"titre": "The Witcher 3", "auteur": "CD Projekt"},
            {"titre": "The Legend of Zelda: Breath of the Wild", "auteur": "Nintendo"},
            {"titre": "Minecraft", "auteur": "Mojang"},
            {"titre": "Red Dead Redemption 2", "auteur": "Rockstar Games"},
            {"titre": "God of War", "auteur": "Santa Monica Studio"},
            {"titre": "Hollow Knight", "auteur": "Team Cherry"},
            {"titre": "Celeste", "auteur": "Matt Makes Games"},
            {"titre": "Super Mario Odyssey", "auteur": "Nintendo"},
            {"titre": "Dark Souls III", "auteur": "FromSoftware"},
            {"titre": "Overwatch", "auteur": "Blizzard Entertainment"}
        ]

        # 2. INSERTION EN BASE
        for u in users_data:
            user = User(
                id=str(uuid.uuid4()),
                nom=u["nom"],
                prenom=u["prenom"],
                mail=u["mail"],
                numero_telephone=u["numero_telephone"],
                nationalite=u["nationalite"]
            )
            db.add(user)

        def add_ressources(data_list, type_str):
            for item in data_list:
                r = Ressource(
                    id=str(uuid.uuid4()),
                    titre=item["titre"],
                    type=type_str,
                    auteur=item["auteur"],
                    disponible=True
                )
                db.add(r)

        add_ressources(livres_data, "Livre")
        add_ressources(films_data,  "Film")
        add_ressources(jeux_data,   "Jeu")

        db.commit()
        print("→ Fixtures insérées avec succès")

    except Exception as e:
        db.rollback()
        print(f"Erreur lors de l'insertion : {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    # Usage : python scripts/load_fixtures.py [--nodrop]
    drop = "--nodrop" not in sys.argv
    main(drop_first=drop)
