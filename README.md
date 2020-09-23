# Rules to Automate Business Logic 
##### Transaction Logic: half the system
For most transaction-oriented database applications, backend database logic
is a substantial portion of the effort.
It includes _multi-table_ derivation and constraint logic,
and actions such as sending mail or messages.

Such backend logic is typically coded in `before_flush` events,
database triggers, and/or stored procedures.
The prevailing assumption is that such *domain-specific logic must surely be 
domain-specific code.*  

##### Problem: Code-intensive - time-consuming, error prone
The problem is that this is a lot of code.  Often nearly half the
effort for a transactional database-oriented systems,
it is time-consuming, complex and error-prone.

##### Rules: 40X more concise, extensible, performant, manageable
This project introduces a _declarative alternative_:
you specify a set of **_spreadsheet-like rules,_**
which are then executed by a login engine operating
as a plugin to sqlalchemy.  As in a spreadsheet,
there are dramatic gains in conciseness and clarity:

* **5 spreadsheet-like rules** implement the check-credit requirement (shown below).
The same logic requires **200 hundred of lines** of code
[(shown here)](../../wiki/by-code) - a factor of 40:1.

* This can represent meaningful improvements in project delivery and agility.
Experience has shown that such rules can address *over 95%* of
the backend logic, reducing such logic by *40X*.

Skeptical?  You should be.  There are many types of rule engines,
and experience has shown they are not appropriate to transaction processing.
For more information, [see Rule Engines](../../wiki/Rules-Engines).

This implementation is specifically designed to meet
the demands of transaction processing:
* Performance - rule execution is optimized to eliminate and optimize SQL
* Extensibility - use Python to extend rule automation
* Manageability - use Python tools for code editing,
debugging, code management, etc

For more information, [see the Rules Engine Overview](../../wiki/Home).


## Architecture
<figure><img src="images/architecture.png" width="500"><figcaption>Architecture</figcaption></figure>


 1. Your logic is **declared** as Python functions (see example below).

 2. Your application makes calls on `sqlalchemy` for inserts, updates and deletes.

    - By bundling transaction logic into sqlalchemy data access, your logic
  is automatically shared, whether for hand-written code (Flask apps, APIs)
  or via generators such as Flask AppBuilder.

 3. The **python-rules** logic engine handles sqlalchemy `before_flush` events on
`Mapped Tables`

 4. The logic engine operates much like a spreadsheet:
**watch** for changes at the attribute level,
**react** by running rules that referenced changed attributes,
which can **chain** to still other attributes that refer to
_those_ changes.  Note these might be in different tables,
providing automation for _multi-table logic_.

Logic does not apply to updates outside sqlalchemy,
nor to sqlalchemy batch updates or unmapped sql updates.


## Declaring Logic as Spreadsheet-like Rules
To illustrate, let's use an adaption
of the Northwind database,
with a few rollup columns added.
For those not familiar, this is basically
Customers, Orders, OrderDetails and Products,
as shown in the diagrams below.

##### Declare rules using Python
Logic is declared as spreadsheet-like rules as shown below
from  [`nw/nw_logic/nw_rules_bank.py`](nw/nw_logic/nw_rules_bank.py),
which implements the *check credit* requirement:
```python
def activate_basic_check_credit_rules():
    """ Check Credit Requirement:
        * the balance must not exceed the credit limit,
        * where the balance is the sum of the unshipped order totals
        * which is the rollup of OrderDetail Price * Quantities:
    """

    Rule.constraint(validate=Customer, as_condition=lambda row: row.Balance <= row.CreditLimit,
                    error_msg="balance ({row.Balance}) exceeds credit ({row.CreditLimit})")
    Rule.sum(derive=Customer.Balance, as_sum_of=Order.AmountTotal,
             where=lambda row: row.ShippedDate is None)  # *not* a sql select sum
    
    Rule.sum(derive=Order.AmountTotal, as_sum_of=OrderDetail.Amount)
   
    Rule.formula(derive=OrderDetail.Amount, as_expression=lambda row: row.UnitPrice * row.Quantity)
    Rule.copy(derive=OrderDetail.UnitPrice, from_parent=Product.UnitPrice)
```

The specification is fully executable, and governs around a
dozen transactions.  Let's look at **Add Order (Check Credit) -**
enter an Order / OrderDetails,
and rollup to AmountTotal / Balance to check CreditLimit.

This representatively complex transaction illustrates
common logic execution patterns, described below.

##### Activate Rules
To test our rules, we use
[`nw/trans_tests/add_order.py`](nw/trans_tests/add_order.py).
It activates the rules using this import:
```python
from nw.nw_logic import session  # opens db, activates logic listener <--
```
 
This executes [`nw/nw_logic/__init__.py`](nw/nw_logic/__init__.py),
which sets up the rule engine:
```python
by_rules = True  # True => use rules, False => use hand code (for comparison)
if by_rules:
    rule_bank_setup.setup(session, engine)     # setup rules engine
    activate_basic_check_credit_rules()        # loads rules above
    rule_bank_setup.validate(session, engine)  # checks for cycles, etc
else:
    # ... conventional after_flush listeners (to see rules/code contrast)
```
This is what replaces 200 lines of conventional code.  Let's see how it operates.

## Logic Execution: Watch, React, Chain
The engine operates much as you might imagine a spreadsheet:

* **Watch** - for inserts, deletes, and updates at the *attribute* level

* **React** - derivation rules referencing changes are (re)executed
(forward chaining *rule inference*); unreferenced rules are pruned.

* **Chain** - if recomputed values are referenced by still other rules,
*these* are re-executed.  Note this can be in other tables, thus
automating multi-table transaction logic.

Let's see how.
   
#### Example: Add Order - Multi-Table Adjustment, Chaining

<figure><img src="images/check-credit.png" width="500"><figcaption>The <b>Add Order</b> example illustrates chaining as OrderDetails are added:
</figcaption></figure>

1. The `OrderDetail.UnitPrice` is referenced from the Product
so it is copied

1. OrderDetails are referenced by the Orders' `AmountTotal` sum rule,
so `AmountTotal` is adjusted (chaining)

1. The `AmountTotal` is referenced by the Customers' `Balance`,
so it is adjusted (chaining)

1. And the Credit Limit constraint is checked 
(exceptions are raised if constraints are violated)

All of the dependency management to see which attribute have changed,
logic ordering, the SQL commands to read and adjust rows, and the chaining
are fully automated by the engine, based solely on the rules above.
This is how 5 rules represent the same logic as 200 lines of code.

Let's explore the multi-table chaining, and how
it's optimized.

##### Optimizations: Multi-table _Adjustment_ (vs. nested `sum` queries)
The `sum` rule that "watches" `OrderDetail.AmountTotal` is in
a different table: `Orders`.  So, the "react" logic has to
perform a multi-table transaction.  And this means we need to
be careful about performance.

Note that rules declare _end conditions_, enabling / _obligating_
the engine to optimize execution (like a SQL query optimizer). 
Consider the rule for `Customer.Balance`.

As in commonly the case (e.g. Rete engines, some ORM systems),
you may reasonably expect this is executed as a SQL `select sum`.

**_It is not._**

Instead, it is executed as an *adjustment:*
as single row update to the Orders balance.
This optimization dramatically reduces the SQL cost,
often by orders of magnitude:

  * `select sum` queries are expensive - imagine a customer with thousands of Orders.
  
  * Here, it's lots worse, since it's a _chained sum_,
  so computing the balance requires not only we read all the orders,
  but all the OrderDetails of each order.

[See here](../../wiki/Multi-Table-Logic-Execution)
for more information on Rule Execution.


## An Agile Perspective
The core tenant of agile is _working software,_
driving _collaboration,_ for _rapid iterations._
Here's how rules can help.

##### Working Software _Now_
The examples above illustrate how just a few rules can replace 
[pages of code](https://github.com/valhuber/python-rules/wiki/by-code).

##### Collaboration - Running Screens

Certainly business users are more easily able to
read rules than code.  But honestly, rules are
pretty abstract.

Business users relate best to actual working pages -
_their_ intepretation of working software.
The [fab-quick-start](https://github.com/valhuber/fab-quick-start/wiki))
project enables you to build a basic web app in minutes.

This project has already generated such an app, which you can run like this
(note: work in progress - constraint error messages not properly shown).

```
cd nw_app
export FLASK_APP=app
flask run
```

##### Iteration - Automatic Ordering
Rules are _self-organizing_ - they recognize their interdependencies,
and order their execution and database access (pruning, adjustments etc)
accordingly.  This means:

* order is independent - you can state the rules in any order
and get the same result

* maintenance is simple - just make changes, additions and deletions,
the engine will reorganize execution order and database access, automatically


## Installation

To get started, you will need:

* Python3.8 (Relies on `from __future__ import annotations`, so requires Python 3.8)

   * Run the windows installer; on mac/Unix, consider [using brew](https://opensource.com/article/19/5/python-3-default-mac#what-to-do)
   
* virtualenv - see [here](https://www.google.com/url?q=https%3A%2F%2Fpackaging.python.org%2Fguides%2Finstalling-using-pip-and-virtual-environments%2F%23creating-a-virtual-environment&sa=D&sntz=1&usg=AFQjCNEu-ZbYfqRMjNQ0D0DqU1mhFpDYmw)  (e.g.,  `pip install virtualenv`)

* An IDE - any will do (I've used [PyCharm](https://www.jetbrains.com/pycharm/download) and [VSCode](https://code.visualstudio.com), install notes [here](https://github.com/valhuber/fab-quick-start/wiki/IDE-Setup)) - ide will do, though different install / generate / run instructions apply for running programs

Issues?  [Try here](https://github.com/valhuber/fab-quick-start/wiki/Mac-Python-Install-Issues).


Using your IDE or command line: 
```
git fork / clone
cd python-rules
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
The project includes:
* the logic engine that executes the rules
* the sample database (sqlite, so no db install is required)
* business logic, both
[by-code](https://github.com/valhuber/python-rules/wiki/by-code) and
[by-rules,](https://github.com/valhuber/python-rules/wiki/by-rules)
to facilitate comparison
   * control whether logic is via rules or code by altering`by_rules` in
   [`__init__.py`](https://github.com/valhuber/python-rules/blob/master/nw/nw_logic/__init__.py)
* a test folder that runs various sample transactions

You can run the programs in the `nw/trans_tests` folder
(note the generated log),
and/or review this readme and the wiki.

## Status: Running, Under Development
Essential functions running on 9/6/2020:
multi-table transactions -
key paths of copy, formula, constraint, sum and event rules. 

Not complete, under active development.  Key remaining items include
delete, and fix constraint messages with Flask / Flask AppBuilder.

Ready to explore and provide feedback
on general value, and features.
