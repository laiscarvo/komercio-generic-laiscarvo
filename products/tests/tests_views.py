from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.views import status

from products.models import Product
from accounts.models import Account


class ProductRegisterandListViewTest(APITestCase):
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

        cls.data_product = {
            "description": "Airpod pro 9.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.user_seller = Account.objects.create_user(**cls.account_data_seller)
        cls.token_seller = Token.objects.create(user=cls.user_seller)

        cls.user_not_seller = Account.objects.create_user(**cls.account_data_not_seller)
        cls.token_not_seller = Token.objects.create(user=cls.user_not_seller)

    def test_can_register_product(self):
        """
        Verifica se somente vendedor pode criar produtos
        """

        url = f"/api/products/"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_not_seller.key)

        response = self.client.post(url, self.data_product)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        msg = f"Verifique se é possivel somente o seller criar produtos"
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_returning_keys_products(self):
        """
        Verifica se as chaves no retorno de criação estão correta
        """

        url = f"/api/products/"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        response = self.client.post(url, self.data_product)

        expected_keys = {
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        }
        result_keys = set(response.data.keys())
        msg = f"Verifique se as chaves retonadas estão corretas"
        self.assertSetEqual(expected_keys, result_keys, msg)

    def test_can_register_product_with_negative_quantity(self):
        """
        Verifica se a quantidade de produtos pode ser somente positiva
        """

        url = f"/api/products/"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        data_product_negative_quantity = {
            "description": "Airpod pro 2.0",
            "price": 100.99,
            "quantity": -1,
        }

        response = self.client.post(url, data_product_negative_quantity)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = f"Verifique se a quantidade de produtos pode ser somente positiva"
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_anyone_can_list_products(self):
        """
        Verifica se qualquer um pode listar produtos
        """
        url_detail = f"/api/products/"

        response = self.client.get(url_detail)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        msg = f"Verifique se é possivel qualquer um listar produtos"
        self.assertEqual(expected_status_code, result_status_code, msg)


class ProductUpdatedViewTest(APITestCase):
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

        cls.data_product = {
            "description": "Airpod pro 9.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.user_seller = Account.objects.create_user(**cls.account_data_seller)
        cls.token_seller = Token.objects.create(user=cls.user_seller)

        cls.user_not_seller = Account.objects.create_user(**cls.account_data_not_seller)
        cls.token_not_seller = Token.objects.create(user=cls.user_not_seller)

        cls.product = Product.objects.create(
            **cls.data_product,
            seller_id=cls.user_seller.id,
        )

    def test_can_update_product(self):
        """
        Verifica se somente vendedor pode atualizar seu produto
        """

        url = f"/api/products/{self.product.id}/"

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        data_update = {"price": 79.99}

        response = self.client.patch(url, data_update)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        msg = f"Verifique se é possivel somente o seller atualizar seu produto"
        self.assertEqual(expected_status_code, result_status_code, msg)
