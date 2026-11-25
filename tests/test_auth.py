import unittest
from app import create_app, db, bcrypt
from app.users.models import User


class AuthSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("dev")
        self.app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        )
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login_pages_load(self):
        """Views Tests: коректне завантаження сторінок реєстрації та входу."""
        resp_register = self.client.get("/users/register")
        self.assertEqual(resp_register.status_code, 200)

        resp_login = self.client.get("/users/login")
        self.assertEqual(resp_login.status_code, 200)

    def test_user_registration_saves_to_db_with_hashed_password(self):
        """Тестування збереження користувача у БД при реєстрації."""
        response = self.client.post(
            "/users/register",
            data={
                "username": "marta_test",
                "email": "marta_test@example.com",
                "password": "secret123",
                "confirm_password": "secret123",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(username="marta_test").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "marta_test@example.com")
        self.assertNotEqual(user.password, "secret123")
        self.assertTrue(bcrypt.check_password_hash(user.password, "secret123"))

    def test_login_and_logout_flow(self):
        """Тестування входу і виходу користувача на сайті."""
        hashed_pw = bcrypt.generate_password_hash("secret123").decode("utf-8")
        user = User(
            username="marta_login",
            email="marta_login@example.com",
            password=hashed_pw,
        )
        db.session.add(user)
        db.session.commit()

        # Неавторизований доступ до /users/account перенаправляє на /users/login
        unauth_resp = self.client.get("/users/account", follow_redirects=False)
        self.assertEqual(unauth_resp.status_code, 302)
        self.assertIn("/users/login", unauth_resp.headers["Location"])

        # Успішний вхід
        login_resp = self.client.post(
            "/users/login",
            data={
                "username": "marta_login",
                "password": "secret123",
            },
            follow_redirects=True,
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("marta_login", login_resp.get_data(as_text=True))

        # Доступ до /users/account після входу
        account_resp = self.client.get("/users/account")
        self.assertEqual(account_resp.status_code, 200)
        self.assertIn("marta_login", account_resp.get_data(as_text=True))

        # Вихід із системи
        logout_resp = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(logout_resp.status_code, 200)

        # Після виходу доступ до /users/account знову закритий
        after_logout_resp = self.client.get("/users/account", follow_redirects=False)
        self.assertEqual(after_logout_resp.status_code, 302)
        self.assertIn("/users/login", after_logout_resp.headers["Location"])


if __name__ == "__main__":
    unittest.main()