For most transaction-oriented database applications, backend database logic
is a substantial portion of the effort, typically nearly half.
This includes multi-table derivation and constraint logic,
and actions such as sending mail or messages.

The prevailing assumption is that such *domain-specific logic must surely be 
domain-specfic code.*  This project introduces a declarative
alternative to such logic, wherein you specify a set of spreadsheet-like
rules, which are then executed by a plugin to sqlalchemy.

This rule-oriented approach confers several advantages
over hand-coding:

| Consideration |      Rules    | Hand-code |
| ------------- | ------------- | --------- |
| **Conciseness**  | **5 spreadsheet-like rules** implement the check-credit requirement (shown below) | The same logic requires **200 hundred of lines** of code [(shown here)](https://github.com/valhuber/python-rules/wiki/by-code)|
| **Performance** | SQLs are *automatically pruned and minimized* (example below)| Optimizations require hand-code, often over-looked due to project time pressure |
| **Quality** | Rules are *automatically re-used* over all transactions, minimizing missed corner-cases| Considerable test and debug is required to find and address all corner cases, with high risk of bugs |
| **Agility** | Rule execution is *automatically re-ordered* per dependencies, simplifying iteration cycles<br><br>Business Users can read the rules, and collaborate<br><br>Collaboration is further supported by running screens - see also Fab-QuickStart below | Changes require code to be re-engineered, at substantial cost and time |

This can represent a meaningful reduction in project delivery.
Experience has shown that such rules can address over 90% of
the backend logic, reducing such logic by 40X (200 vs. 5).

### Background
The subject database is an adaption of the Northwind database,
with a few rollup columns added.
For those not familiar, this is basically
Customers, Orders, OrderDetails and Products.

#### Architecture
<img src="https://github.com/valhuber/python-rules/blob/master/images/architecture.png" width="500">

1. Your application makes calls on `sqlalchemy` for inserts, updates and deletes.
This code can be hand-written, or via generators such as Flask AppBuilder
2. The logic engine handles sqlalchemy `before_flush` events on
`Mapped Tables.`
3. Your logic is expressed as Python functions (see example below).
Debug your logic with logs that show which rules execute,
and breakpoints in formula/constraint/action rules
expressed in Python.

Logic does not apply to updates outside sqlalchemy,
or to sqlalchemy batch updates or unmapped sql updates.

#### Declaring Logic
Logic is declared as spreadsheet-like rules as shown below
from  [`nw_rules_bank.py`](https://github.com/valhuber/python-rules/blob/master/nw/nw_logic/nw_rules_bank.py),
activated in [`__init__.py`](https://github.com/valhuber/python-rules/blob/master/nw/nw_logic/__init__.py).
The logic below implements the *check credit* requirement:
* *the balance must not exceed the credit limit,*
* *where the balance is the sum of the unshipped order totals*
* *which is the rollup of OrderDetail Price * Quantities:*
```python
Logic.constraint_rule(validate="Customer",
                      as_condition="row.Balance <= row.CreditLimit")
Logic.sum_rule(derive="Customer.Balance", as_sum_of="OrderList.AmountTotal",
               where="row.ShippedDate is None")

Logic.sum_rule(derive="Order.AmountTotal", as_sum_of="OrderDetailList.Amount")

Logic.formula_rule(derive="OrderDetail.Amount",
                   as_exp="row.UnitPrice * row.Quantity")
Logic.copy_rule(derive="OrderDetail.UnitPrice", from_parent="ProductOrdered.UnitPrice")
```
The specification is fully executable, and governs around a
dozen transactions.  Here we look at 2 simple examples:

* **Add Order (Check Credit) -** enter an order/orderdetails,
and rollup to AmountTotal / Balance to check CreditLimit

* **Ship / Unship an Order (Adjust Balance) -** when an Order's `DateShippped`
is changed, adjust the Customers 'Balance`

These representatively complex transactions illustrate common patterns:

##### Adjustments
Rollups provoke an important design choice: store the aggregate,
or sum things on the fly.  There are cases for both:
   - **Sum** - use sql `select sum` queries to add child data as required.
   This eliminates consistency risks with storing redundant data
   (i.e, the aggregate becomes invalid if an application fails to
   adjust it in *all* of the cases).
   
   - **Stored Aggregates** - a good choice when data volumes are large, and / or chain,
   since the application can **adjust** (make a 1 row update) the aggregate based on the
   *delta* of the children.

This design decision can dominate application coding.  It's nefarious,
since data volumes may not be known whn coding begins.  (Ideally, this can be
a "late binding" decision, like a sql index.)

The logic engine uses the **Stored Aggregate** approach.  This optimizes
multi-table update logic chaining, where updates to 1 row
trigger updates to other rows, which further chain to still more rows.

Here, the stored aggregates are `Customer.Balance`, and `Order.AmountTotal`
(a *chained* aggregate).  Consider the **ship / unship order** example:
* if `ShippedDate` *is not* altered, nothing is dependent on that,
so the rule is **pruned** from the logic execution.
The logic engine issues a 1-row update to the Order

* if `ShippedDate` *is* altered, the logic engine **adjusts** the `Customer.Balance`
with a 1 row update.
  * Contrast this to approaches in other systems where
the balance is recomputed with expensive aggregate queries over *all*
the customers' orders, and *all* their OrderDetails.

  *   Imagine, for example, a customer might have
   thousands of Orders, each with thousands of OrderDetails.

##### State Transition Logic (old values)
Logic often depends on the old and new state of a row.
For example, we need to adjust the Customers balance
if the Orders `ShippedDate` is changed.

##### DB-generated Keys
DB-generated keys are often tricky (how do you insert
items if you don't know the db-generated orderId?), shown here in `Order`
and `OrderDetail`.  These were well-handled by sqlalchemy,
where adding OrderDetail rows into the Orders' collection automatically
set the foreign keys.

### Installation
Using your IDE or command line: 
```
git clone
cd python-rules
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
The project includes:
* the logic engine that executes the rules
* the sample database (sqlite, so no db install is required)
* business logic, both by code an by rules,
to facilitate comparison
   * select by-hand vs. rules logic in the `nw_logic/__init__.py` file
* a test folder that runs various sample transactions

You can run the programs in the `nw/trans-tests` folder,
and/or review this readme and the wiki.

#### Status: Running, Under Development
Essential functions running on 9/6/2020: able to save order (a multi-table transaction - certain paths of copy, formula, constraint and sum rules).  Not complete, under active development.

### Explore
The [by-code](https://github.com/valhuber/python-rules/wiki/by-code)
and [by-rules](https://github.com/valhuber/python-rules/wiki/by-rules)
approaches are described in the 
[wiki](https://github.com/valhuber/python-rules/wiki).


### Flask App Builder
You can also run an app (generated by [fab-quick-start](https://github.com/valhuber/fab-quick-start/wiki))
to exolore the `nw` database, though this is not currently enforcing logic.

Fab-quick-start builds default web apps in just a few minutes.  Such working software can support agile business / IT collaboration.

```
cd nw-app
export FLASK_APP=app
flask run
```
