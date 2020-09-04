from logic_engine.logic import Logic


def check_balance(row, old_row, logic_row) -> bool:
    return row.balance <= row.creditLimit


def compute_amount(row, old_row, logic_row):
    return row.UnitPrice * row.Quantity


Logic.constraint_rule(validate="Customer", calling='check_balance')
Logic.sum_rule(derive="Customer.balance", as_sum_of="Order.AmountTotal", where="ShippedDate not None")
Logic.count_rule(derive="Customer.OrderCount", as_count_of="Order", where="ShippedDate not None")
Logic.sum_rule(derive="Order.AmountTotal", as_sum_of="OrderDetails.Amount")
Logic.formula_rule(derive="OrderDetail.Amount", calling=compute_amount)
Logic.copy_rule(derive="OrderDetail.UnitPrice", from_parent="Product.UnitPrice")
