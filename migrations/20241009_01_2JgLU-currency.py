"""
currency
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
 """
            create table if not exists currency (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                symbol VARCHAR(255) UNIQUE NOT NULL
            );
       """,
            "drop table if exists currency cascade;"
         ),
    step(
       """
            insert into currency (name, symbol)
            values ('BTCUSDT', 'BTC'),
                   ('ETHUSDT', 'ETH'),
                   ('BNBUSDT', 'BNB'),
                   ('DOGEUSDT', 'DOGE')
            on conflict do nothing;
       """
    )
]
