"""
currency
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
    """
    CREATE TABLE IF NOT EXISTS currency (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            symbol VARCHAR(255) UNIQUE NOT NULL
        );
    """,
        "DROP TABLE currency;"
         )
]
