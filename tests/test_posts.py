import unittest
from app import create_app, db
from app.posts.models import Post

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        """Тест створення поста (User Story 01)"""
        with self.app.app_context():
            response = self.client.post(
                "/post/create",
                data={
                    "title": "My first post",
                    "content": "This is TDD content!",
                    "category": "news",
                    "is_active": "y"
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post added successfully", response.data)

            post = db.session.scalar(db.select(Post).where(Post.title == "My first post"))
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD content!")
            self.assertEqual(post.author, "Anonymous")

    def test_get_posts_list(self):
        """Тест списку постів (User Story 02)"""
        with self.app.app_context():
            p = Post(title="TDD List Post", content="List Content", category="tech", is_active=True)
            db.session.add(p)
            db.session.commit()

            response = self.client.get("/post")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"TDD List Post", response.data)

    def test_detail_post(self):
        """Тест деталей поста (User Story 03)"""
        with self.app.app_context():
            p = Post(title="Single Post", content="Deep details text", category="publication")
            db.session.add(p)
            db.session.commit()
            p_id = p.id

            response = self.client.get(f"/post/{p_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Deep details text", response.data)

    def test_update_post(self):
        """Тест редагування поста (User Story 04)"""
        with self.app.app_context():
            p = Post(title="Old Title", content="Old Content", category="other")
            db.session.add(p)
            db.session.commit()
            p_id = p.id

            response = self.client.post(
                f"/post/{p_id}/update",
                data={
                    "title": "New Title",
                    "content": "Updated Content",
                    "category": "other",
                    "is_active": "y"
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            updated = db.session.get(Post, p_id)
            self.assertEqual(updated.title, "New Title")

    def test_delete_post(self):
        """Тест видалення поста (User Story 05)"""
        with self.app.app_context():
            p = Post(title="For Delete", content="Delete me", category="news")
            db.session.add(p)
            db.session.commit()
            p_id = p.id

            response = self.client.post(f"/post/{p_id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            deleted = db.session.get(Post, p_id)
            self.assertIsNone(deleted)

if __name__ == "__main__":
    unittest.main()
    