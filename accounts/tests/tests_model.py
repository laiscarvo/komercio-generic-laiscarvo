from django.test import TestCase
from accounts.models import Account


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.account_data = {
            "username": "pedro",
            "password": "1234",
            "first_name": "pedro",
            "last_name": "Alves",
            "is_seller": True,
        }

        cls.account = Account.objects.create_user(**cls.account_data)

        cls.account.save()

    def test_username_max_length(self):
        """
        Verifica a propriedade de tamanho máximo de `username`
        """

        expected_max_length = 50

        result_max_length = Account._meta.get_field("username").max_length

        msg = f"Verifique se a propriedade `max_length` de username foi definida como {expected_max_length}"

        self.assertEqual(expected_max_length, result_max_length, msg)

    def test_first_name_max_length(self):
        """
        Verifica a propriedade de tamanho máximo de `first_name`
        """

        expected_max_length = 50

        result_max_length = Account._meta.get_field("first_name").max_length

        msg = f"Verifique se a propriedade `max_length` de first_name foi definida como {expected_max_length}"

        self.assertEqual(expected_max_length, result_max_length, msg)

    def test_last_name_max_length(self):
        """
        Verifica a propriedade de tamanho máximo de `last_name`
        """

        expected_max_length = 50

        result_max_length = Account._meta.get_field("last_name").max_length

        msg = f"Verifique se a propriedade `max_length` de  last_name foi definida como {expected_max_length}"

        self.assertEqual(expected_max_length, result_max_length, msg)

    def test_username_can_be_unique(self):
        """
        Verifica a propriedade unique de `username`
        """
        unique = Account._meta.get_field("username").unique
        msg = f"Verifique a propriedade `unique` de  username"

        self.assertTrue(unique, msg)
