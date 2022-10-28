from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.views import status


class AccountRegisterViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = "/api/accounts/"
        cls.account_data_seller = {
            "username": "ana",
            "password": "abcd",
            "first_name": "ana",
            "last_name": "alves",
            "is_seller": True,
        }
        cls.account_data_not_seller = {
            "username": "amanda",
            "password": "abcd",
            "first_name": "amanda",
            "last_name": "alves",
            "is_seller": False,
        }

    def test_can_register_seller(self):
        """
        Verifica a criação de um usuario vendedor
        """
        response = self.client.post(self.register_url, self.account_data_seller)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = f"Verifique se o status_code da criação de usuario vendendor foi definido como {expected_status_code}"

        self.assertEqual(expected_status_code, result_status_code, msg)

        account_count = Account.objects.count()
        expected_count = 1

        self.assertEqual(expected_count, account_count)

    def test_can_register_not_seller(self):
        """
        Verifica a criação de um usuario vendedor
        """
        response = self.client.post(self.register_url, self.account_data_not_seller)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = f"Verifique se o status_code da criação de usuario foi definido como {expected_status_code}"

        self.assertEqual(expected_status_code, result_status_code, msg)

        account_count = Account.objects.count()
        expected_count = 1

        self.assertEqual(expected_count, account_count)

    def test_if_password_is_being_hashed(self):
        """
        Verifica se a senha foi hasheada da maneira correta
        """
        self.client.post(self.register_url, self.account_data_seller)

        account = Account.objects.first()

        is_password_hashed = account.check_password(
            self.account_data_seller["password"]
        )
        msg = f"Verifique se a senha está sendo hasheada da maneira correta"

        self.assertTrue(is_password_hashed, msg)

    def test_returning_keys_user_seller(self):
        response = self.client.post(self.register_url, self.account_data_seller)
        expected_keys = {
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "is_active",
            "is_superuser",
            "date_joined",
        }
        result_keys = set(response.data.keys())
        msg = f"Verifique se as chaves retonadas estão corretas"

        self.assertSetEqual(expected_keys, result_keys, msg)

    def test_returning_keys_user_not_seller(self):
        """
        Verifica se as chaves retornadas na response estão corretas
        """
        response = self.client.post(self.register_url, self.account_data_not_seller)
        expected_keys = {
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "is_active",
            "is_superuser",
            "date_joined",
        }

        result_keys = set(response.data.keys())
        msg = f"Verifique se as chaves retonadas estão corretas"

        self.assertSetEqual(expected_keys, result_keys, msg)


class AccountLoginViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_url = "/api/login/"
        cls.account_data_seller = {
            "username": "ana",
            "password": "abcd",
            "first_name": "ana",
            "last_name": "alves",
            "is_seller": True,
        }
        cls.account_data_not_seller = {
            "username": "amanda",
            "password": "abcd",
            "first_name": "amanda",
            "last_name": "alves",
            "is_seller": False,
        }

        cls.user_seller = Account.objects.create_user(**cls.account_data_seller)
        cls.token = Token.objects.create(user=cls.user_seller)

        cls.user_not_seller = Account.objects.create_user(**cls.account_data_not_seller)
        cls.token_not_seller = Token.objects.create(user=cls.user_not_seller)

    def test_correct_login_seller(self):
        """
        Verifica o login de um usuario vendedor
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.login_url, self.account_data_seller)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        msg = f"Verifique se o status_code do login de usuario vendendor foi definido como {expected_status_code}"

        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_response_data = {"token": self.token.key}
        result_response_data = response.data
        msg_1 = f"Verifique se a response do login de usuario vendendor foi definido como {expected_response_data}"

        self.assertEqual(expected_response_data, result_response_data, msg_1)

    def test_correct_login_not_seller(self):
        """
        Verifica o login de um usuario
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_not_seller.key)
        response = self.client.post(self.login_url, self.account_data_not_seller)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        msg = f"Verifique se o status_code do login de usuario foi definido como {expected_status_code}"

        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_response_data = {"token": self.token_not_seller.key}
        result_response_data = response.data
        msg_1 = f"Verifique se a response do login de usuario foi definido como {expected_response_data}"

        self.assertEqual(expected_response_data, result_response_data, msg_1)


class AccountViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account_data_seller = {
            "username": "ana",
            "password": "abcd",
            "first_name": "ana",
            "last_name": "alves",
            "is_seller": True,
        }
        cls.account_data_not_seller = {
            "username": "amanda",
            "password": "abcd",
            "first_name": "amanda",
            "last_name": "alves",
            "is_seller": False,
        }

        cls.user_seller = Account.objects.create_user(**cls.account_data_seller)
        cls.token_seller = Token.objects.create(user=cls.user_seller)

        cls.user_not_seller = Account.objects.create_user(**cls.account_data_not_seller)
        cls.token_not_seller = Token.objects.create(user=cls.user_not_seller)

    def test_can_updated_owner(self):
        """
        Verifica se somente dono da conta pode atualizar
        """

        url_detail = f"/api/accounts/{self.user_seller.id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_not_seller.key)

        data_update = {"last_name": "alves de lima"}

        response = self.client.patch(url_detail, data_update)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        msg = f"Verifique se é possivel somente o dono da conta fazer updates"
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_only_superuser_can_disable(self):
        """
        Verifica se somente o superuser pode desativar a conta
        """

        url_detail = f"/api/accounts/{self.user_seller.id}/management/"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        data_update = {"is_active": False}

        response = self.client.patch(url_detail, data_update)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        msg = f"Verifique se é possivel somente o superuser desativar a conta"
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_only_superuser_can_activate(self):
        """
        Verifica se somente o superuser pode ativar a conta
        """

        url_detail = f"/api/accounts/{self.user_seller.id}/management/"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        data_update = {"is_active": True}

        response = self.client.patch(url_detail, data_update)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        msg = f"Verifique se é possivel somente o superuser ativar a conta"
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_anyone_can_list_users(self):
        """
        Verifica se qualquer um pode listar usuários
        """

        url_detail = f"/api/accounts/newest/{1}/"

        response = self.client.get(url_detail)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        msg = f"Verifique se é possivel qualquer um listar usuários"
        self.assertEqual(expected_status_code, result_status_code, msg)


"""
 OK - teste criacao de conta seller
 OK - teste criacao de conta not seller
 OK - teste chaves erradas seller
 OK - teste chaves erradas not seller
 OK - teste login seller retorna token 
 OK - teste login not seller retorna token 
 OK - teste somente dono da conta pode atualizar
 OK - teste somente adm pode desativar 
 OK - teste somente adm pode ativar
 OK - teste qlq um pode listar usuarios 
"""
