"""
currency_price
"""

from yoyo import step

__depends__ = {'20240925_03_n3Yea-currency-pair'}
steps = [
    step(
    """
        CREATE TABLE currency_price (
            id SERIAL PRIMARY KEY,
            currency_pair_id INTEGER REFERENCES currency_pair(id),
            price FLOAT NOT NULL,
            source VARCHAR(50) NOT NULL,
            datetime TIMESTAMP NOT NULL
        );
    """,
        "DROP TABLE currency_price;"
         )
]
