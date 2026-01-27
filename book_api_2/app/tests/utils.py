def register_and_login(client, username, password):
    client.post("/auth/register", params={"username": username, "password": password})
    r = client.post("/auth/login", data={"username": username, "password": password})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}