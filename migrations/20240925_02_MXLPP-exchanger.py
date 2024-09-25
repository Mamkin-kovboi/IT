"""
exchanger
"""

from yoyo import step

__depends__ = {'20240925_01_cVP8O-currency'}

steps = [
    step(
    """
        CREATE TABLE IF NOT EXISTS exchanger (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            api_url VARCHAR(255) UNIQUE NOT NULL
        );
    """,
        "DROP TABLE exchanger;"
         )
]
