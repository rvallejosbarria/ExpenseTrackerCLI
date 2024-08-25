class Expense:
  def __init__(self, expense_id, expense_date, description, category, amount, currency, created_at, updated_at) -> None:
    self.id = expense_id
    self.expense_date = expense_date
    self.description = description
    self.category = category
    self.amount = amount
    self.currency = currency
    self.created_at = created_at
    self.updated_at = updated_at

  def __str__(self):
    return f"\"{self.description}\" (ID: {self.id}) created at: {self.expense_date}"

  def to_dict(self):
    return {
      "id": self.id,
      "expense_date": self.expense_date,
      "description": self.description,
      "category": self.category,
      "amount": self.amount,
      "currency": self.currency,
      "created_at": self.created_at,
      "updated_at": self.updated_at
    }

  @staticmethod
  def from_dict(data):
    return Expense(data["id"], data["expense_date"], data["description"], data["category"], data["amount"], data["currency"], data["created_at"], data["updated_at"])