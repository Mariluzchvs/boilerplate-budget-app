class Category:
  def __init__(self, name):
    self.name= name
    self.total= 0.0
    self.ledger= []

  def __repr__(self):
    line= f"{self.name:*^30}\n"
    account= 0

    for item in self.ledger:
      line+= f"{item['description'][:23]:<23}{item['amount']:>7.2f}\n"
      account+= item["amount"]

    line+= f"Total: {self.total:.2f}"
    return line

  def deposit(self, amount, description= ""):
    self.total+= amount
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, *args):
    can_withdraw= self.check_funds(amount)

    description= args[0] if args else ""

    if can_withdraw:
      self.total-= amount
      self.ledger.append({"amount": -amount, "description": description})
      
    return can_withdraw

  def get_balance(self):
    return self.total

  def transfer(self, amount, instance):
    can_transfer= self.check_funds(amount)

    if can_transfer:
      self.withdraw(amount, f"Transfer to {instance.name}")
      instance.deposit(amount, f"Transfer from {self.name}")
      
    return can_transfer

  def check_funds(self, amount):
    if amount> self.total:
      return False
    return True

  
food = Category("Food")
entertainment= Category("Entertainment")
food.deposit(100, "potatoes")
food.transfer(50, entertainment)
#food.withdraw(20, "rice")
#print(food.ledger)
#print(str(food))
#print(entertainment.ledger)
#print(food.get_balance())
#print(entertainment.get_balance())

def create_spend_chart(categories):
  desc= "Percentage spent by category\n"

  total=0
  cats= {}
  for cat in categories:
    cat_total= 0
    for item in cat.ledger:
      amount= item["amount"]
      if amount<0:
        total+= abs(amount)
        cat_total+= abs(amount)

    cats[cat.name] =(cat_total)
  #print(cats)

  cats = {
    k: (v / total) * 100
    for k, v in cats.items()
  }

  dash_width = len(cats) * 3 + 1
  spaces = dash_width - 1
  for n in range(100, -1, -10):
    desc += f"{n:>3}| "
    bar_row= []
    for value in cats.values():
      row_value= [" "] *3
      if value >= n:
        row_value[0] = "o"
      bar_row+= row_value
    desc += f"{''.join(bar_row)}{' ' * (spaces - len(bar_row))}\n"

  desc += f"{' ' * 4}{'-' * dash_width}\n"

  cat_names = [list(name) for name in cats]
  while any(cat_names):
    desc += f"{' ' * 4}"
    for name in cat_names:
      desc += f" {' ' if not name else name.pop(0)} "
    desc += " \n"
    
  desc = desc.strip() + '  '

  return desc

  #print(categories)
  #print(categories[0].ledger)


create_spend_chart([food, entertainment])
