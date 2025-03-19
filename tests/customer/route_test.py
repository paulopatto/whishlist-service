from sqlmodel import select

from src.customer.data import CustomerModel


def describe_customer_creation():
    def describe_when_pass_correct_params():
        def should_returns_created_status(test_client, session, valid_customer):
            response = test_client.post(
                "/api/customer",
                json={
                    "name": valid_customer.name,
                    "email": valid_customer.email
                }
            )
            assert response.status_code == 201

        def should_user_present_at_database(test_client, session, valid_customer):
            # Arrange
            _ = test_client.post(
                "/api/customer",
                json={
                    "name": valid_customer.name,
                    "email": valid_customer.email
                }
            )
            # Act
            with session:
                statement = select(CustomerModel).where(
                    CustomerModel.email == valid_customer.email
                )
                result = session.exec(statement)
                created_customer = result.one()

            # Assert
            assert created_customer is not None
            assert created_customer.name == valid_customer.name
            assert created_customer.email == valid_customer.email


    def describe_when_not_pass_correct_params():
        def should_returns_unprocessed_entity(test_client, session):
            response = test_client.post("/api/customer", json={})
            assert response.status_code == 422

