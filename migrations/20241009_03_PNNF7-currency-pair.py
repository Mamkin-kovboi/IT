"""
currency_pair
"""

from yoyo import step

__depends__ = {'20241009_02_6RNdc-exchanger'}

steps = [
    step(
  """
            create table if not exists currency_pair (
                id serial primary key,
                currency_from_id integer not null references currency(id) on delete cascade,
                currency_to_id integer not null references currency(id) on delete cascade,
                exchanger_id integer not null references exchanger(id) on delete cascade
            );
        """,
        """
            drop table if exists currency_pair cascade;
        """
     ),
    step(
        """
            insert into currency_pair (currency_from_id, currency_to_id, exchanger_id) values
                ((select id from currency where name='BTCUSDT'),
                (select id from currency where name='DOGEUSDT'),
                (select id from exchanger where name='Bybit')),

                ((select id from currency where name='ETHUSDT'),
                (select id from currency where name='BNBUSDT'),
                (select id from exchanger where name='Binance')),

                ((select id from currency where name='DOGEUSDT'),
                (select id from currency where name='BTCUSDT'),
                (select id from exchanger where name='Bybit')),

                ((select id from currency where name='BNBUSDT'),
                (select id from currency where name='ETHUSDT'),
                (select id from exchanger where name='Binance'));
        """
    ),
    step(
        """
            select
                currency.name,
                currency.symbol,
                exchanger.api_url
            from
                currency
            inner join
                currency_pair on currency_pair.currency_from_id = currency.id
            inner join
                exchanger on currency_pair.exchanger_id = exchanger.id;
        """
    )

]
