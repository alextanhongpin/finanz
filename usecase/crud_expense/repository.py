class Repository:
    expenses = []
    id = 0

    def create(self, exp):
        self.id += 1
        exp.id = self.id
        self.expenses.append(exp)
        return exp

    def list(self):
        return self.expenses
