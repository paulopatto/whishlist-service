def describe_healthcheck_route():
    def test_get_healthcheck_path(test_client):
        response = test_client.get("/api/healthcheck")

        body = response.json()

        assert response.status_code == 200
        assert body["status"] == "ok"

