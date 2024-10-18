"""
currency
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE SCHEMA myschema;
        """,
    ),
    step(
  """
            create table if not exists myschema.currency (
                id serial primary key,
                name varchar(255) not null,
                symbol varchar(255) not null
            );
        """,
        """
            drop table if exists currency cascade;
        """

    ),
    step(
        """
            insert into myschema.currency (name, symbol)
            values ('BTCUSDT', 'BTC'),
                   ('ETHUSDT', 'ETH'),
                   ('BNBUSDT', 'BNB'),
                   ('DOGEUSDT', 'DOGE')
            on conflict do nothing;
        """
    )
]
