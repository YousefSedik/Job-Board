import factory
from django.contrib.auth import get_user_model
from users.models import Resume

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # email = factory.LazyAttribute(lambda obj: f"{obj.email}@example.com")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class ResumeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resume

    user = factory.SubFactory(UserFactory)
    resume = factory.django.FileField(filename="resume.pdf")