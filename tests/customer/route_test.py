def describe_customer_creation_route():
    def describe_when_pass_correct_params():
        def should_returns_created_status(test_client, db_session):
            response = test_client.post(
                "/api/customer", json={"name": "Test", "email": "test@example.org"}
            )
            assert response.status_code == 201

    def describe_when_not_pass_correct_params():
        def should_returns_unprocessed_entity(test_client, db_session):
            response = test_client.post("/api/customer", json={})
            assert response.status_code == 422

