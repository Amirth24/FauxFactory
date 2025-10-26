import faker
from faker.providers import phone_number

__faker_instance = None


def get_faker() -> faker.Faker:
    """Get a configured Faker instance."""
    global __faker_instance
    if __faker_instance is None:
        faker_instance = faker.Faker()
        faker.add_provider(phone_number)

    return faker_instance
