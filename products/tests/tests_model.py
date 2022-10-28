from itertools import product
from django.test import TestCase
from accounts.models import Account
from products.models import Product


class ProductRelationshipTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account_data = {
            "username": "ivete",
            "password": "abcd",
            "first_name": "ivete",
            "last_name": "anjos",
            "is_seller": True,
        }
        cls.account_data_2 = {
            "username": "ana",
            "password": "abcd",
            "first_name": "ana",
            "last_name": "anjos",
            "is_seller": True,
        }

        cls.product_data_1 = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.product_data_2 = {
            "description": "Smartband Mi 7.0",
            "price": 120.99,
            "quantity": 15,
        }

        cls.seller = Account.objects.create(**cls.account_data)

        cls.product: Product = Product.objects.create(
            **cls.product_data_1,
            seller_id=cls.seller.id,
        )

        cls.product.save()

    def test_one_to_many_relationship_with_account(self):
        """
        Verifica se um product pode estar associado a somente um seller
        """
        self.seller_2 = Account.objects.create(**self.account_data_2)
        self.product.seller_id = self.seller_2.id

        expected = self.product.seller.username
        result = self.account_data_2["username"]
        msg = "Verique se a relação de product e account está correta"

        # print(expected)
        # print(result)
        # print(msg)

        self.assertEqual(expected, result, msg)

    def test_one_to_many_relationship_with_account_1(self):
        """
        Verifica se um account pode estar associado a muitos products
        """
        self.product_1 = Product.objects.create(
            **self.product_data_2,
            seller_id=self.seller.id,
        )

        expected = self.product.seller.username
        result = self.product_1.seller.username
        msg = "Verique se a relação de account  e product está correta"

        # print(expected)
        # print(result)
        # print(msg)

        self.assertEqual(expected, result, msg)
