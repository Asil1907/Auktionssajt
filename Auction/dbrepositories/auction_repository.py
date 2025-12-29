from database import get_db

class AuctionRepository:

    @staticmethod
    def get_all():
        return get_db().execute(
            "SELECT * FROM auctions ORDER BY id DESC"
        ).fetchall()

    @staticmethod
    def get_active():
        return get_db().execute(
            """
            SELECT * FROM auctions
            WHERE datetime(end_datetime) > datetime('now')
            ORDER BY end_datetime ASC
            """
        ).fetchall()

    @staticmethod
    def get_by_id(auction_id):
        return get_db().execute(
            "SELECT * FROM auctions WHERE id = ?",
            (auction_id,)
        ).fetchone()

    @staticmethod
    def search(keyword):
        return get_db().execute(
            """
            SELECT * FROM auctions
            WHERE title LIKE ?
            ORDER BY id DESC
            """,
            (f"%{keyword}%",)
        ).fetchall()

    @staticmethod
    def create(title, description, starting_bid, end_datetime):
        db = get_db()
        db.execute(
            """
            INSERT INTO auctions (title, description, starting_bid, end_datetime)
            VALUES (?, ?, ?, ?)
            """,
            (title, description, starting_bid, end_datetime)
        )
        db.commit()

    @staticmethod
    def delete(auction_id):
        db = get_db()
        db.execute(
            "DELETE FROM auctions WHERE id = ?",
            (auction_id,)
        )
        db.commit()

    @staticmethod
    def like(auction_id):
        db = get_db()
        db.execute(
            "UPDATE auctions SET likes = likes + 1 WHERE id = ?",
            (auction_id,)
        )
        db.commit()

    @staticmethod
    def dislike(auction_id):
        db = get_db()
        db.execute(
            "UPDATE auctions SET dislikes = dislikes + 1 WHERE id = ?",
            (auction_id,)
        )
        db.commit()
