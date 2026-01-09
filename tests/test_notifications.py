def notif_payload(event_type="review.created", payload='{"user_id":1,"tmdb_movie_id":123,"rating":8}'):
    return {"event_type": event_type, "payload": payload}

def test_create_notification_ok(client):
    r = client.post("/api/notifications", json=notif_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["id"] >= 1
    assert data["event_type"] == "review.created"

def test_list_notifications_returns_list(client):
    client.post("/api/notifications", json=notif_payload())
    r = client.get("/api/notifications")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1

def test_get_notification_404(client):
    r = client.get("/api/notifications/999999")
    assert r.status_code == 404

def test_delete_then_404(client):
    r = client.post("/api/notifications", json=notif_payload(event_type="x", payload="y"))
    notif_id = r.json()["id"]

    r1 = client.delete(f"/api/notifications/{notif_id}")
    assert r1.status_code == 204

    r2 = client.delete(f"/api/notifications/{notif_id}")
    assert r2.status_code == 404
