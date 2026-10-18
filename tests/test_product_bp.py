import unittest
from app import app

class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list_page(self):
        """Тест маршруту каталогу /products/."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop".encode("utf-8"), response.data)
        self.assertIn("Phone".encode("utf-8"), response.data)
        self.assertIn("PC".encode("utf-8"), response.data)

    def test_product_detail_page(self):
        """Тест сторінки окремого товару /products/<id>."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop".encode("utf-8"), response.data)
        self.assertIn(b"1200", response.data)

    def test_product_not_found(self):
        """Тест на неіснуючий товар (помилка 404)."""
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()