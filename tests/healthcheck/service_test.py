from src.healthcheck.interfaces import HealthCheckResultDTO
from src.healthcheck.services import database_is_health, server_is_health


def describe_healthcheck_service():
    def describe_server_is_health():
        def test_message_type():
            response = server_is_health()
            assert type(response) is HealthCheckResultDTO

        def test_health_truthy():
            response = server_is_health()
            assert response.health is True

    def describe_database_is_health():
        def test_message_type():
            response = database_is_health()
            assert type(response) is HealthCheckResultDTO

        def test_health_truthy():
            response = database_is_health()
            assert response.health is True
