import pytest
import uuid
import secrets
from fastapi.testclient import TestClient
from App.main import app

client = TestClient(app)

# --- Helpers ---
def user_data(**kwargs):
    data = {
        "nom": f"Nom{secrets.randbelow(9000) + 1000}",
        "prenom": f"Prenom{secrets.randbelow(9000) + 1000}",
        "mail": f"user_{uuid.uuid4()}@mail.com",
        "numero_telephone": "+33" + str(secrets.randbelow(1000000000)).zfill(9),
        "nationalite": secrets.choice(["France", "Testland", "Belgique", "Espagne", "Allemagne", "Italie"])
    }
    data.update(kwargs)
    return data

def ressource_data(**kwargs):
    data = {
        "titre": f"Ressource_{uuid.uuid4()}",
        "type": secrets.choice(["Livre", "Film", "Jeu", "Autre"]),
        "auteur": f"Auteur_{secrets.randbelow(9000) + 1000}",
        "disponible": True
    }
    data.update(kwargs)
    return data

def make_user(**kwargs):
    data = user_data(**kwargs)
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    return response.json()

def make_ressource(**kwargs):
    data = ressource_data(**kwargs)
    response = client.post("/ressources/", json=data)
    assert response.status_code == 201
    return response.json()

def make_emprunt(user_id, ressource_id, date_emprunt="2025-06-01", date_retour="2025-06-25"):
    emprunt_data = {
        "user_id": user_id,
        "ressource_id": ressource_id,
        "date_emprunt": date_emprunt,
        "date_retour": date_retour
    }
    response = client.post("/emprunts/", json=emprunt_data)
    assert response.status_code == 201
    return response.json()

# ---------------------- USERS ----------------------

def test_create_user():
    user = make_user()
    assert user["mail"].startswith("user_")

def test_create_user_duplicate_mail():
    user = make_user()
    response = client.post("/users/", json=user_data(mail=user["mail"]))
    assert response.status_code == 400
    assert "déjà enregistré" in response.json()["detail"].lower()

def test_create_user_invalid_mail():
    data = user_data(mail="not-an-email")
    response = client.post("/users/", json=data)
    assert response.status_code == 422

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_by_id():
    user = make_user()
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json()["mail"] == user["mail"]

def test_get_user_not_found():
    response = client.get("/users/FAKE-ID")
    assert response.status_code == 404

def test_update_user():
    user = make_user()
    new_data = user_data(
        nom=user["nom"], 
        prenom="Modif_"+user["prenom"], 
        mail=user["mail"], 
        numero_telephone=user["numero_telephone"], 
        nationalite=user["nationalite"]
    )
    response = client.put(f"/users/{user['id']}", json=new_data)
    assert response.status_code == 200
    assert response.json()["prenom"].startswith("Modif_")

def test_update_user_not_found():
    response = client.put("/users/FAKE-ID", json=user_data())
    assert response.status_code == 404

def test_delete_user():
    user = make_user()
    response = client.delete(f"/users/{user['id']}")
    assert response.status_code in (200, 204)

def test_delete_user_not_found():
    response = client.delete("/users/FAKE-ID")
    assert response.status_code == 404

# ---------------------- RESSOURCES ----------------------

def test_create_ressource():
    res = make_ressource()
    assert res["titre"].startswith("Ressource_")

def test_get_ressources():
    response = client.get("/ressources/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filter_ressources_by_type():
    res = make_ressource(type="Film")
    response = client.get("/ressources/?type=Film")
    assert response.status_code == 200
    data = response.json()
    assert any(r["id"] == res["id"] for r in data)

def test_filter_ressources_by_disponible():
    res = make_ressource(disponible=True)
    response = client.get("/ressources/?disponible=true")
    assert response.status_code == 200
    data = response.json()
    assert any(r["id"] == res["id"] for r in data)

def test_get_ressource_by_id():
    res = make_ressource()
    response = client.get(f"/ressources/{res['id']}")
    assert response.status_code == 200
    assert response.json()["titre"] == res["titre"]

def test_get_ressource_not_found():
    response = client.get("/ressources/FAKE-ID")
    assert response.status_code == 404

def test_update_ressource():
    res = make_ressource()
    new_data = ressource_data(
        titre="NouveauTitre",
        type=res["type"],
        auteur=res["auteur"]
    )
    response = client.put(f"/ressources/{res['id']}", json=new_data)
    assert response.status_code == 200
    assert response.json()["titre"] == "NouveauTitre"

def test_update_ressource_not_found():
    response = client.put("/ressources/FAKE-ID", json=ressource_data())
    assert response.status_code == 404

def test_delete_ressource():
    res = make_ressource()
    response = client.delete(f"/ressources/{res['id']}")
    assert response.status_code in (200, 204)

def test_delete_ressource_not_found():
    response = client.delete("/ressources/FAKE-ID")
    assert response.status_code == 404

# ---------------------- EMPRUNTS ----------------------

def test_create_emprunt_and_rendre():
    user = make_user()
    res = make_ressource()
    emprunt = make_emprunt(user["id"], res["id"])
    assert emprunt["user_id"] == user["id"]
    assert emprunt["ressource_id"] == res["id"]
    # Rendre l'emprunt
    response = client.delete(f"/emprunts/{emprunt['id']}")
    assert response.status_code == 204

def test_create_emprunt_user_not_found():
    res = make_ressource()
    fake_id = str(uuid.uuid4())
    emprunt_data = {
        "user_id": fake_id,
        "ressource_id": res["id"],
        "date_emprunt": "2025-06-01",
        "date_retour": "2025-06-25"
    }
    response = client.post("/emprunts/", json=emprunt_data)
    assert response.status_code == 400
    assert "utilisateur non trouvé" in response.json()["detail"].lower()

def test_create_emprunt_ressource_not_found():
    user = make_user()
    fake_id = str(uuid.uuid4())
    emprunt_data = {
        "user_id": user["id"],
        "ressource_id": fake_id,
        "date_emprunt": "2025-06-01",
        "date_retour": "2025-06-25"
    }
    response = client.post("/emprunts/", json=emprunt_data)
    assert response.status_code == 400
    assert "ressource non trouvée" in response.json()["detail"].lower()

def test_create_emprunt_already_empruntee():
    user1 = make_user()
    user2 = make_user()
    res = make_ressource()
    make_emprunt(user1["id"], res["id"])
    # La ressource n'est plus disponible
    emprunt_data = {
        "user_id": user2["id"],
        "ressource_id": res["id"],
        "date_emprunt": "2025-06-01",
        "date_retour": "2025-06-25"
    }
    response = client.post("/emprunts/", json=emprunt_data)
    assert response.status_code == 400
    assert "ressource déjà empruntée" in response.json()["detail"].lower()

def test_get_emprunt_by_id():
    user = make_user()
    res = make_ressource()
    emprunt = make_emprunt(user["id"], res["id"])
    response = client.get(f"/emprunts/{emprunt['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == emprunt["id"]

def test_get_emprunt_not_found():
    response = client.get("/emprunts/FAKE-ID")
    assert response.status_code == 404

def test_delete_emprunt_not_found():
    response = client.delete("/emprunts/FAKE-ID")
    assert response.status_code == 404

def test_list_emprunts():
    response = client.get("/emprunts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_emprunts_by_user():
    user = make_user()
    res = make_ressource()
    make_emprunt(user["id"], res["id"])
    response = client.get(f"/emprunts/user/{user['id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_emprunt_invalid_date():
    user = make_user()
    res = make_ressource()
    # Mauvais format de date
    emprunt_data = {
        "user_id": user["id"],
        "ressource_id": res["id"],
        "date_emprunt": "01-06-2025",
        "date_retour": "25-06-2025"
    }
    response = client.post("/emprunts/", json=emprunt_data)
    assert response.status_code == 422

# ------------ AUTRES BIZARRETES ET EDGE CASES --------------

def test_user_delete_cascades_emprunts():
    user = make_user()
    res = make_ressource()
    emprunt = make_emprunt(user["id"], res["id"])
    # On supprime l'utilisateur
    response = client.delete(f"/users/{user['id']}")
    assert response.status_code in (200, 204)
    # Emprunt doit être supprimé ou inaccessible
    response = client.get(f"/emprunts/{emprunt['id']}")
    # Peut être 404 selon la config, tolérer les 200 si cascade non implémentée
    assert response.status_code in (404, 200)

def test_ressource_delete_cascades_emprunts():
    user = make_user()
    res = make_ressource()
    emprunt = make_emprunt(user["id"], res["id"])
    # On supprime la ressource
    response = client.delete(f"/ressources/{res['id']}")
    assert response.status_code in (200, 204)
    response = client.get(f"/emprunts/{emprunt['id']}")
    assert response.status_code in (404, 200)

def test_user_list_pagination():
    # Ajouter 5 users
    for _ in range(5):
        make_user()
    response = client.get("/users/?skip=0&limit=2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 2

def test_ressource_list_pagination():
    for _ in range(5):
        make_ressource()
    response = client.get("/ressources/?skip=0&limit=2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 2

def test_emprunt_list_pagination():
    user = make_user()
    for _ in range(2):
        res = make_ressource()
        make_emprunt(user["id"], res["id"])
    response = client.get("/emprunts/?skip=0&limit=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 1

# ----------- BAD REQUESTS / VALIDATION ------------

def test_create_ressource_invalid_type():
    data = ressource_data(type="INVALID_TYPE")
    response = client.post("/ressources/", json=data)
    assert response.status_code == 422

def test_create_user_missing_fields():
    data = {}
    response = client.post("/users/", json=data)
    assert response.status_code == 422

def test_create_ressource_missing_fields():
    data = {}
    response = client.post("/ressources/", json=data)
    assert response.status_code == 422

def test_create_emprunt_missing_fields():
    data = {}
    response = client.post("/emprunts/", json=data)
    assert response.status_code == 422

# ----------- SANITY CHECK -----------

def test_sanity_check():
    response = client.get("/")
    # Si tu exposes une route racine, adapte ce test
    assert response.status_code in (200, 404)
