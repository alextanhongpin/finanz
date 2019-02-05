class Repository:
    expenses = []
    id = 0

    def __init__(self, pool):
        self._pool = pool

    async def get(self):
        async with (await self._pool.Connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT 1 + 1')
                data = cursor.fetchone()
        await self._pool.close()
        return data

    def create(self, exp):
        self.id += 1
        exp.id = self.id
        self.expenses.append(exp)
        return exp

    def list(self):
        return self.expenses
