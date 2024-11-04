from typing import List

from poetry.repositories import Repository


class CurrencyPairRepository(Repository):
        """ Currency_Pair Repository"""

        @collect_response
        async def create(self, cmd: models.CreateCurrencyCommand) -> models.Currency:
            q = """
                    insert into currency(
                        name, symbol
                    ) values (
                        %(name)s, %(symbol)s
                    )
                    returning id, name, symbol
                """
            async with get_connection() as cur:
                await cur.execute(q, cmd.to_dict())
                return await cur.fetchone()

        @collect_response
        async def read(self, query: models.ReadCurrencyQuery) -> models.Currency:
            q = """
                    select
                        id, name, symbol
                    from cities
                    where id = %(id)s
                """
            async with get_connection() as cur:
                await cur.execute(q, query.to_dict())
                return await cur.fetchone()

        @collect_response
        async def read_all(self) -> List[models.Currency]:
            q = """
                    select
                        id, name, symbol
                    from currency
                """
            async with get_connection() as cur:
                await cur.execute(q)
                return await cur.fetchall()

        @collect_response
        async def update(self, cmd: models.UpdateCurrencyCommand) -> models.Currency:
            q = """
                    update currency
                    set
                        name = %(name)s,
                        symbol = %(symbol)s,
                    where id = %(id)s
                    returning id, name, symbol
                """
            async with get_connection() as cur:
                await cur.execute(q, cmd.to_dict())
                return await cur.fetchone()

        @collect_response
        async def delete(self, cmd: models.DeleteCurrencyCommand) -> models.Currency:
            q = """
                    delete from currency
                    where id = %(id)s
                    returning id, name, symbol
                """
            async with get_connection() as cur:
                await cur.execute(q, cmd.to_dict())
                return await cur.fetchone()