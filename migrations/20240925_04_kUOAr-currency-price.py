"""
currency_price
"""

from yoyo import step

__depends__ = {'20240925_03_n3Yea-currency-pair'}
steps = [
    step(
    """
        create table if not exists currency_price (
            id SERIAL PRIMARY KEY,
            currency_pair_id INTEGER REFERENCES currency_pair(id),
            price FLOAT NOT NULL,
            source VARCHAR(50) NOT NULL,
            datetime TIMESTAMP NOT NULL
        );
    """,
        "drop table if exists currency_price cascade;"
         )
]
