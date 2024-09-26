"""
exchanger
"""

from yoyo import step

__depends__ = {'20240925_01_cVP8O-currency'}

steps = [
    step(
    """
        create table if not exists exchanger (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            api_url VARCHAR(255) UNIQUE NOT NULL
        );
    """,
        "drop table if exists exchanger cascade;"
         ),
    step(
        """
            insert into exchanger (name, api_url)
            values ('Bybit', 'https://api.bybit.com/spot/v3/public/quote/ticker/price'),
                   ('Binance', 'https://api.binance.com/api/v3/ticker/price');
        """,
        "drop table if exists exchanger cascade"
        )
]
