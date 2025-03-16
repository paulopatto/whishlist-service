from src.healthcheck.services import check_status


def describe_healthcheck_service():
    def test_check_status():
        response = check_status()
        assert response == "Everything is ok"

