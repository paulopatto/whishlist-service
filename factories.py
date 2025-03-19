import factory
from faker import Faker

from src.customer.data import CustomerModel

faker = Faker()


class CustomerFactory(factory.Factory):
    class Meta:
        model = CustomerModel

    name = factory.LazyAttribute(lambda _: faker.name())
    email = factory.LazyAttribute(lambda _: faker.email())


class InvalidUserFactory(CustomerFactory):
    email = None
