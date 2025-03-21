
from src.customer.data import CustomerModel


def helper_arrange_customer_at_database_to_edit(session, valid_customer):
    with session:
        customer = CustomerModel(
            name=valid_customer.name,
            email=valid_customer.email
        )
        session.add(customer)
        session.commit()
        session.refresh(customer)
        external_id = customer.external_id
        return external_id

def helper_request_patch_to_update_customer(
        test_client, session,
        valid_customer,
        external_id,
        data_to_update
    ):
    return test_client.patch(
        f"/api/customer/{external_id}",
        json=data_to_update,
        headers={ "Authorization": "Bearer valid_api_key" }
    )
