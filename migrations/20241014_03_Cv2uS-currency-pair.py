"""
currency-pair
"""

from yoyo import step

__depends__ = {'20241014_02_9hS8q-exchanger'}

steps = [
    step(
  """
            create table if not exists myschema.currency_pair (
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
            insert into myschema.currency (name, symbol)
            values ('BTCUSDT', 'BTC'),
                   ('ETHUSDT', 'ETH'),
                   ('BNBUSDT', 'BNB'),
                   ('DOGEUSDT', 'DOGE')
            on conflict do nothing;
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

    ),
    step(
        """
            insert into myschema.currency_pair (currency_from_id, currency_to_id, exchanger_id) values
                ((select id from myschema.currency where name='BTCUSDT'),
                (select id from myschema.currency where name='DOGEUSDT'),
                (select id from myschema.exchanger where name='Bybit')),

                ((select id from myschema.currency where name='ETHUSDT'),
                (select id from myschema.currency where name='BNBUSDT'),
                (select id from myschema.exchanger where name='Binance')),

                ((select id from myschema.currency where name='DOGEUSDT'),
                (select id from myschema.currency where name='BTCUSDT'),
                (select id from myschema.exchanger where name='Bybit')),

                ((select id from myschema.currency where name='BNBUSDT'),
                (select id from myschema.currency where name='ETHUSDT'),
                (select id from myschema.exchanger where name='Binance'));
        """
    ),
    step(
        """
            select
                myschema.currency.name,
                myschema.currency.symbol,
                myschema.exchanger.api_url
            from
                myschema.currency
            inner join
                myschema.currency_pair on currency_pair.currency_from_id = currency.id
            inner join
                myschema.exchanger on currency_pair.exchanger_id = exchanger.id;
        """
    )

]

