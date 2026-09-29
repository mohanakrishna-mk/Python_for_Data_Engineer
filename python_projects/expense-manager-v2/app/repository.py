from datetime import datetime

from database import get_connection


class TransactionRepository:

    def add(self, transaction):

        with get_connection() as connection:

            connection.execute("""
                INSERT INTO transactions
                (type, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                transaction.type,
                transaction.amount,
                transaction.category,
                transaction.description,
                transaction.date.isoformat()
            ))

    def get_all(self):

        with get_connection() as connection:

            cursor = connection.execute("""
                SELECT *
                FROM transactions
                ORDER BY date DESC
            """)

            return cursor.fetchall()

    def delete(self, transaction_id):

        with get_connection() as connection:

            cursor = connection.execute("""
                DELETE FROM transactions
                WHERE id = ?
            """, (transaction_id,))

            return cursor.rowcount