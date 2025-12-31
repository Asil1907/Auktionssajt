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
    def create(title, description, starting_bid, end_datetime, category='Övrigt'):
        db = get_db()
        db.execute(
            """
            INSERT INTO auctions (title, description, starting_bid, end_datetime, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, description, starting_bid, end_datetime, category)
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

    @staticmethod
    def get_all_categories():
        """Hämta alla unika kategorier"""
        result = get_db().execute(
            "SELECT DISTINCT category FROM auctions WHERE category IS NOT NULL ORDER BY category"
        ).fetchall()
        return [row['category'] for row in result]

    @staticmethod
    def filter_auctions(category=None, min_price=None, max_price=None, show_all=False):
        """Filtrera auktioner efter kategori och prisintervall"""
        query = "SELECT * FROM auctions WHERE 1=1"
        params = []
        
        # Filtrera endast pågående om inte show_all
        if not show_all:
            query += " AND datetime(end_datetime) > datetime('now')"
        
        # Filtrera efter kategori
        if category and category != 'Alla':
            query += " AND category = ?"
            params.append(category)
        
        # Filtrera efter min pris
        if min_price:
            query += " AND starting_bid >= ?"
            params.append(min_price)
        
        # Filtrera efter max pris
        if max_price:
            query += " AND starting_bid <= ?"
            params.append(max_price)
        
        query += " ORDER BY end_datetime ASC"
        
        return get_db().execute(query, params).fetchall()
