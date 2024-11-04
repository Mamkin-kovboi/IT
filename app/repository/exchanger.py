from typing import List

from poetry.repositories import Repository


class ExchangerRepository (Repository):
        """ Exchanger Repository"""

        @collect_response
        async def create(self, cmd: models.CreateCurrencyCommand) -> models.Exchanger:
            q = """
                    insert into exchanger(
                        name, api_url
                    ) values (
                        %(name)s, %(api_url)s
                    )
                    returning id, name, api_url
                """
            async with get_connection() as cur:
                await cur.execute(q, cmd.to_dict())
                return await cur.fetchone()

        @collect_response
        async def read(self, query: models.ReadExchangerQuery) -> models.Exchanger:
            q = """
                    select
                        id, name, api_url
                    from exchanger
                    where id = %(id)s
                """
            async with get_connection() as cur:
                await cur.execute(q, query.to_dict())
                return await cur.fetchone()

        @collect_response
        async def read_all(self) -> List[models.Exchanger]:
            q = """
                    select
                        id, name, api_url
                    from exchanger
                """
            async with get_connection() as cur:
                await cur.execute(q)
                return await cur.fetchall()

        @collect_response
        async def update(self, cmd: models.UpdateExchangerCommand) -> models.Exchanger:
            q = """
                    update exchanger
                    set
                        name = %(name)s,
                        api_url = %(api_url)s,
                    where id = %(id)s
                    returning id, name, api_url
                """
            async with get_connection() as cur:
                await cur.execute(q, cmd.to_dict())
                return await cur.fetchone()

        @collect_response
        async def delete(self, cmd: models.DeleteExchangerCommand) -> models.Exchanger:
            q = """
                    delete from exchanger
                    where id = %(id)s
                    returning id, name, api_url
                """
            async with get_connection() as cur:
                await cur.execute(q, cmd.to_dict())
                return await cur.fetchone()