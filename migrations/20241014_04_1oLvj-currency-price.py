"""
currency-price
"""

from yoyo import step

__depends__ = {'20241014_03_Cv2uS-currency-pair'}

steps = [
    step(
  """
            create table if not exists myschema.currency_price (
                id serial primary key,
                currency_pair_id integer references currency_pair(id),
                price float not null,
                source varchar(50) not null,
                datetime timestamp not null
            );
        """,
        """
            drop table if exists currency_price cascade;
        """
    )
]
