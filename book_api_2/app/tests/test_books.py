from .utils import register_and_login

def test_create_book(client):
    headers = register_and_login(client, "user1", "pass123")

    r = client.post(
        "/books/",
        json={"title": "1984", "author": "Orwell", "year": 1949},
        headers=headers
    )

    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "1984"


def test_list_books(client):
    headers = register_and_login(client, "user1", "pass123")

    client.post("/books/", json={"title": "Dune", "author": "Herbert", "year": 1965}, headers=headers)

    r = client.get("/books/")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_update_own_book(client):
    headers = register_and_login(client, "user1", "pass123")

    r = client.post("/books/", json={"title": "Old", "author": "A", "year": 2000}, headers=headers)
    book_id = r.json()["id"]

    r = client.put(
        f"/books/{book_id}",
        json={"title": "New", "author": "B", "year": 2024},
        headers=headers
    )

    assert r.status_code == 200
    assert r.json()["title"] == "New"


def test_cannot_update_others_book(client):
    headers1 = register_and_login(client, "user1", "pass123")
    headers2 = register_and_login(client, "user2", "pass123")

    r = client.post("/books/", json={"title": "Secret", "author": "A", "year": 2000}, headers=headers1)
    book_id = r.json()["id"]

    r = client.put(
        f"/books/{book_id}",
        json={"title": "Hack", "author": "B", "year": 2024},
        headers=headers2
    )

    assert r.status_code == 403


def test_delete_book(client):
    headers = register_and_login(client, "user1", "pass123")

    r = client.post("/books/", json={"title": "Temp", "author": "A", "year": 2000}, headers=headers)
    book_id = r.json()["id"]

    r = client.delete(f"/books/{book_id}", headers=headers)
    assert r.status_code == 200


def test_cannot_create_without_login(client):
    r = client.post("/books/", json={"title": "X", "author": "Y", "year": 2000})
    assert r.status_code == 401