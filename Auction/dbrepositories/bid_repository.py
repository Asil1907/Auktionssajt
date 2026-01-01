from database import get_db
from datetime import datetime

class BidRepository:

    @staticmethod
    def create(auction_id, bidder, amount):
        db = get_db()
        db.execute(
            """
            INSERT INTO bids (auction_id, bidder, amount, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (auction_id, bidder, amount, datetime.now().isoformat())
        )
        db.commit()

    @staticmethod
    def get_top_two(auction_id):
        return get_db().execute(
            """
            SELECT * FROM bids
            WHERE auction_id = ?
            ORDER BY amount DESC
            LIMIT 2
            """,
            (auction_id,)
        ).fetchall()

    @staticmethod
    def count_for_auction(auction_id):
        return get_db().execute(
            """
            SELECT COUNT(*) as count
            FROM bids
            WHERE auction_id = ?
            """,
            (auction_id,)
        ).fetchone()["count"]

    @staticmethod
    def get_highest(auction_id):
        return get_db().execute(
            """
            SELECT MAX(amount) as highest
            FROM bids
            WHERE auction_id = ?
            """,
            (auction_id,)
        ).fetchone()["highest"]

    @staticmethod
    def get_all_for_auction(auction_id):
        """Hämta alla bud för en auktion"""
        return get_db().execute(
            """
            SELECT * FROM bids
            WHERE auction_id = ?
            ORDER BY amount DESC, created_at DESC
            """,
            (auction_id,)
        ).fetchall()

    @staticmethod
    def delete(bid_id):
        """Ta bort ett bud"""
        db = get_db()
        db.execute(
            "DELETE FROM bids WHERE id = ?",
            (bid_id,)
        )
        db.commit()

    
    
