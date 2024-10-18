"""
exchanger
"""

from yoyo import step

__depends__ = {'20241014_01_i10RF-currency'}

steps = [
    step(
  """
            create table if not exists myschema.exchanger (
                id serial primary key,
                name varchar(255) not null,
                api_url varchar(255) not null
            );
        """,
        """
            drop table if exists exchanger cascade;
        """
    ),
    step(
  """
            insert into myschema.exchanger (name, api_url)
            values ('Bybit', 'https://api.bybit.com/spot/v3/public/quote/ticker/price'),
                   ('Binance', 'https://api.binance.com/api/v3/ticker/price');
        """,
        """
            drop table if exists exchanger cascade;
        """

    )
]

