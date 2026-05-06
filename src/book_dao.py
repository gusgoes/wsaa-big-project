import mysql.connector
from config.dbconfig import DB_CONFIG
class BookDAO:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def get_connection(self):
        """Create and return a database connection and cursor."""
        self.connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        self.cursor = self.connection.cursor(dictionary=True)
        return self.connection, self.cursor

    def close_connection(self):
        """Close the cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create(self, book_data):
        """Insert a new book into the database."""
        connection, cursor = self.get_connection()
        sql = "INSERT INTO book (title, author, price) VALUES (%s, %s, %s)"
        values = (book_data['title'], book_data['author'], book_data['price'])
        cursor.execute(sql, values)
        connection.commit()
        new_id = cursor.lastrowid
        self.close_connection()
        return new_id

    def get_all(self):
        """Return all books from the database."""
        connection, cursor = self.get_connection()
        cursor.execute("SELECT * FROM book")
        results = cursor.fetchall()
        self.close_connection()
        return results

    def find_by_id(self, id):
        """Return a single book by its ID."""
        connection, cursor = self.get_connection()
        cursor.execute("SELECT * FROM book WHERE id = %s", (id,))
        result = cursor.fetchone()
        self.close_connection()
        return result

    def update(self, id, book_data):
        """Update an existing book."""
        connection, cursor = self.get_connection()
        sql = "UPDATE book SET title = %s, author = %s, price = %s WHERE id = %s"
        values = (book_data['title'], book_data['author'], book_data['price'], id)
        cursor.execute(sql, values)
        connection.commit()
        rows_affected = cursor.rowcount
        self.close_connection()
        return rows_affected

    def delete(self, id):
        """Delete a book by its ID."""
        connection, cursor = self.get_connection()
        cursor.execute("DELETE FROM book WHERE id = %s", (id,))
        connection.commit()
        rows_affected = cursor.rowcount
        self.close_connection()
        return rows_affected

# Create a singleton instance for reuse
book_dao = BookDAO()