import io
import unittest
from app import app
from app.products.views import db, products_table

class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування тестового середовища перед кожним тестом."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False  
        self.client = app.test_client()

        products_table.truncate()

        self.test_product_id = products_table.insert({
            "name": "Тестовий товар",
            "content": "Опис тестового товару",
            "price": 999.99,
            "category": "electronics",
            "quantity": 5,
            "image": None,
            "created_at": "2026-11-04 12:00:00"
        })
        products_table.update({"id": self.test_product_id}, doc_ids=[self.test_product_id])

    def tearDown(self):
        """Очищення бази після завершення тесту."""
        products_table.truncate()

    def test_product_list_page(self):
        """Тест сторінки каталогу /products/."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий товар".encode("utf-8"), response.data)

    def test_product_detail_page(self):
        """Тест сторінки окремого товару /products/<id>."""
        response = self.client.get(f"/products/{self.test_product_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий товар".encode("utf-8"), response.data)
        self.assertIn(b"999.99", response.data)

    def test_product_add_post(self):
        """Тест створення нового товару через POST-запит."""
        data = {
            "name": "Новий смарт-годинник",
            "content": "Опис смарт-годинника",
            "price": "2500.00",
            "category": "electronics",
            "quantity": "10",
            "image": (io.BytesIO(b"fake image data"), "watch.png")
        }
        response = self.client.post("/products/add", data=data, content_type="multipart/form-data", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Новий смарт-годинник".encode("utf-8"), response.data)

    def test_product_delete(self):
        """Тест видалення товару /products/<id>/delete."""
        response = self.client.post(f"/products/{self.test_product_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        product = products_table.get(doc_id=self.test_product_id)
        self.assertIsNone(product)

    def test_product_not_found(self):
        """Тест на неіснуючий товар (помилка 404)."""
        response = self.client.get("/products/99999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()