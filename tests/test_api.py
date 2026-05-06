"""
Integration tests for the Books REST API.

Uses Flask's built-in test client — the server does NOT need to be running,
but MySQL must be running and the wsaa database must exist (run init_db.py first).

Run from the project/ folder:
    python -m pytest tests/ -v
    # or
    python -m unittest discover -s tests -v
"""

import sys
import os
import json
import unittest

# Allow imports from project root (src/, config/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import app


class TestBooksAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self._created_ids = []  # track IDs to clean up after each test

    def tearDown(self):
        # Delete any books created during the test so tests stay independent
        for book_id in self._created_ids:
            self.client.delete(f'/books/{book_id}')

    def _create_book(self, title='Test Book', author='Test Author', price=9.99):
        """Helper: POST a book and return the response. Registers ID for cleanup."""
        payload = {'title': title, 'author': author, 'price': price}
        resp = self.client.post(
            '/books',
            data=json.dumps(payload),
            content_type='application/json'
        )
        if resp.status_code == 201:
            data = json.loads(resp.data)
            self._created_ids.append(data['data']['id'])
        return resp

    # ------------------------------------------------------------------
    # GET /books
    # ------------------------------------------------------------------

    def test_get_all_books_returns_list(self):
        resp = self.client.get('/books')
        self.assertEqual(resp.status_code, 200)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'success')
        self.assertIsInstance(body['data'], list)

    # ------------------------------------------------------------------
    # POST /books  — happy path
    # ------------------------------------------------------------------

    def test_create_book_returns_201_and_id(self):
        resp = self._create_book(title='Clean Code', author='Robert Martin', price=29.99)
        self.assertEqual(resp.status_code, 201)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'success')
        self.assertIn('id', body['data'])
        self.assertIsInstance(body['data']['id'], int)

    # ------------------------------------------------------------------
    # GET /books/<id>
    # ------------------------------------------------------------------

    def test_get_book_by_id_returns_correct_fields(self):
        create_resp = self._create_book(title='The Pragmatic Programmer', author='Hunt & Thomas', price=35.00)
        book_id = json.loads(create_resp.data)['data']['id']

        resp = self.client.get(f'/books/{book_id}')
        self.assertEqual(resp.status_code, 200)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'success')
        data = body['data']
        self.assertEqual(data['id'], book_id)
        self.assertEqual(data['title'], 'The Pragmatic Programmer')
        self.assertEqual(data['author'], 'Hunt & Thomas')
        self.assertAlmostEqual(float(data['price']), 35.00, places=2)

    def test_get_book_not_found_returns_404(self):
        resp = self.client.get('/books/999999')
        self.assertEqual(resp.status_code, 404)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'error')
        self.assertIn('message', body)

    # ------------------------------------------------------------------
    # PUT /books/<id>  — happy path
    # ------------------------------------------------------------------

    def test_update_book_returns_200_and_updated_id(self):
        create_resp = self._create_book(title='Old Title', author='Old Author', price=5.00)
        book_id = json.loads(create_resp.data)['data']['id']

        payload = {'title': 'New Title', 'author': 'New Author', 'price': 15.00}
        resp = self.client.put(
            f'/books/{book_id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['data']['updated'], book_id)

    def test_update_book_persists_changes(self):
        create_resp = self._create_book(title='Before Update', author='Some Author', price=10.00)
        book_id = json.loads(create_resp.data)['data']['id']

        self.client.put(
            f'/books/{book_id}',
            data=json.dumps({'title': 'After Update', 'author': 'New Author', 'price': 20.00}),
            content_type='application/json'
        )

        get_resp = self.client.get(f'/books/{book_id}')
        data = json.loads(get_resp.data)['data']
        self.assertEqual(data['title'], 'After Update')
        self.assertAlmostEqual(float(data['price']), 20.00, places=2)

    def test_update_book_not_found_returns_404(self):
        payload = {'title': 'X', 'author': 'Y', 'price': 1}
        resp = self.client.put(
            '/books/999999',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 404)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'error')

    # ------------------------------------------------------------------
    # DELETE /books/<id>
    # ------------------------------------------------------------------

    def test_delete_book_returns_200_and_deleted_id(self):
        create_resp = self._create_book(title='To Be Deleted', author='Author', price=1.00)
        book_id = json.loads(create_resp.data)['data']['id']
        # Remove from cleanup list since we're deleting it here
        self._created_ids.remove(book_id)

        resp = self.client.delete(f'/books/{book_id}')
        self.assertEqual(resp.status_code, 200)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['data']['deleted'], book_id)

    def test_delete_book_removes_it_from_db(self):
        create_resp = self._create_book(title='Gone Soon', author='Author', price=1.00)
        book_id = json.loads(create_resp.data)['data']['id']
        self._created_ids.remove(book_id)

        self.client.delete(f'/books/{book_id}')

        get_resp = self.client.get(f'/books/{book_id}')
        self.assertEqual(get_resp.status_code, 404)

    def test_delete_book_not_found_returns_404(self):
        resp = self.client.delete('/books/999999')
        self.assertEqual(resp.status_code, 404)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'error')

    # ------------------------------------------------------------------
    # Validation — POST
    # ------------------------------------------------------------------

    def test_create_missing_title_returns_400(self):
        payload = {'author': 'Author', 'price': 9.99}
        resp = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'error')
        self.assertIn('message', body)

    def test_create_empty_title_returns_400(self):
        payload = {'title': '   ', 'author': 'Author', 'price': 9.99}
        resp = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_missing_author_returns_400(self):
        payload = {'title': 'Title', 'price': 9.99}
        resp = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_non_numeric_price_returns_400(self):
        payload = {'title': 'Title', 'author': 'Author', 'price': 'free'}
        resp = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_negative_price_returns_400(self):
        payload = {'title': 'Title', 'author': 'Author', 'price': -1}
        resp = self.client.post('/books', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_zero_price_is_valid(self):
        resp = self._create_book(title='Free Book', author='Author', price=0)
        self.assertEqual(resp.status_code, 201)

    def test_create_no_body_returns_400(self):
        resp = self.client.post('/books', content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    # ------------------------------------------------------------------
    # Validation — PUT
    # ------------------------------------------------------------------

    def test_update_missing_field_returns_400(self):
        create_resp = self._create_book()
        book_id = json.loads(create_resp.data)['data']['id']

        payload = {'title': 'Updated Title'}  # missing author and price
        resp = self.client.put(
            f'/books/{book_id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)
        body = json.loads(resp.data)
        self.assertEqual(body['status'], 'error')


if __name__ == '__main__':
    unittest.main()
