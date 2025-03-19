from sqlmodel import select

from src.customer.data import CustomerModel
from tests.customer.routes_helpers import helper_arrange_customer_at_database_to_edit, helper_request_patch_to_update_customer


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

    def describe_when_pass_email_already_registered():
        def should_returns_conflict(test_client, session, valid_customer):
            # Arrange
            _ = test_client.post(
                "/api/customer",
                json={
                    "name": valid_customer.name,
                    "email": valid_customer.email
                }
            )
            # Act
            response = test_client.post(
                "/api/customer",
                json={
                    "name": valid_customer.name,
                    "email": valid_customer.email
                }
            )
            # Assert
            assert response.status_code == 409

    def describe_when_not_pass_correct_params():
        def should_returns_unprocessed_entity(test_client, session):
            response = test_client.post("/api/customer", json={})
            assert response.status_code == 422

def describe_customer_deletion():
    def describe_when_pass_external_id_not_existent_params():
        """"
        Tenho de confesar que esse teste aqui o copilot sugeriu e ai Eu incluí, não me elimina por causa disso.
        """
        def should_returns_not_found(test_client, session):
            # Act
            response = test_client.delete("/api/customer/123e4567-e89b-12d3-a456-426614174000")

            # Assert
            assert response.status_code == 404

    def should_returns_204_no_content(test_client, session, valid_customer):
        # Arrange
        with session:
            customer = CustomerModel(
                name=valid_customer.name,
                email=valid_customer.email
            )
            session.add(customer)
            session.commit()
            session.refresh(customer)
            external_id = customer.external_id

        # Act
        response = test_client.delete(f"/api/customer/{external_id}")

        # Assert
        assert response.status_code == 204

    def should_delete_customer_by_external_id(test_client, session, valid_customer):
        # Arrange
        with session:
            customer = CustomerModel(
                name=valid_customer.name,
                email=valid_customer.email
            )
            session.add(customer)
            session.commit()
            session.refresh(customer)
            external_id = customer.external_id

        # Act
        response = test_client.delete(f"/api/customer/{external_id}")

        # Assert
        with session:
            statement = select(CustomerModel).where(CustomerModel.external_id == external_id)
            result = session.exec(statement).first()
            assert result is None

def describe_customer_update():
    def describe_given_a_customer_at_the_database():
        def describe_when_pass_new_data_to_update():
            def should_returns_200_ok(test_client, session, valid_customer):
                # Arrange
                eid = helper_arrange_customer_at_database_to_edit(session, valid_customer)
                new_data = {
                    "name": "Updated Name",
                    "email": valid_customer.email  # Mantém o mesmo email
                }
                # Act
                response = helper_request_patch_to_update_customer(test_client, session, valid_customer, eid, data_to_update=new_data)
                # Assert
                assert response.status_code == 200

            def should_update_customer_name_at_database(test_client, session, valid_customer):
                # Arrange
                eid = helper_arrange_customer_at_database_to_edit(session, valid_customer)
                new_data = {
                    "name": "Updated Name",
                    "email": valid_customer.email  # Mantém o mesmo email
                }

                #Act
                response = helper_request_patch_to_update_customer(test_client, session, valid_customer, eid, data_to_update=new_data)

                # Assert
                with session:
                    statement = select(CustomerModel).where(CustomerModel.external_id == eid)
                    result = session.exec(statement).one_or_none()
                    assert result is not None
                    assert result.name == new_data["name"]

def describe_fetch_customer():
    def describe_when_customer_not_exists():
        def should_returns_not_found(test_client, session):
            # Act
            response = test_client.get("/api/customer/123e4567-e89b-12d3-a456-426614174000")
            # Assert
            assert response.status_code == 404

    def describe_when_customer_exists():
        def should_returns_success(test_client, session, valid_customer):
            # Arrange
            with session:
                customer = CustomerModel(
                    name=valid_customer.name,
                    email=valid_customer.email
                )
                session.add(customer)
                session.commit()
                session.refresh(customer)
                external_id = customer.external_id

            # Act
            response = test_client.get(f"/api/customer/{external_id}")

            # Assert
            assert response.status_code == 200

        def should_return_customer_data(test_client, session, valid_customer):
            # Arrange
            with session:
                customer = CustomerModel(
                    name=valid_customer.name,
                    email=valid_customer.email
                )
                session.add(customer)
                session.commit()
                session.refresh(customer)
                external_id = customer.external_id

            # Act
            response = test_client.get(f"/api/customer/{external_id}")

            # Assert
            response_data = response.json()
            assert response_data["id"] == str(external_id)
            assert response_data["name"] == valid_customer.name
            assert response_data["email"] == valid_customer.email

        def should_return_customer_data_if_find_by_email(test_client, session, valid_customer):
            # Arrange
            with session:
                customer = CustomerModel(
                    name=valid_customer.name,
                    email=valid_customer.email
                )
                session.add(customer)
                session.commit()
                session.refresh(customer)
                external_id = customer.external_id

            # Act
            response = test_client.get(f"/api/customer/{customer.email}")

            # Assert
            response_data = response.json()
            assert response_data["id"] == str(external_id)
            assert response_data["name"] == valid_customer.name
            assert response_data["email"] == valid_customer.email
