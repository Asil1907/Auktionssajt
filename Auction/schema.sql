DROP TABLE IF EXISTS bids;
DROP TABLE IF EXISTS auctions;

CREATE TABLE auctions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    starting_bid REAL NOT NULL,
    end_datetime TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0
);

CREATE TABLE bids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auction_id INTEGER NOT NULL,
    bidder TEXT NOT NULL,
    amount REAL NOT NULL,
    created_at TEXT NOT NULL
);

INSERT INTO auctions (title, description, starting_bid, end_datetime)
VALUES (
    'Testauktion 1',
    'En testauktion för att visa funktionalitet',
    100,
    '2025-12-31 23:59'
);

