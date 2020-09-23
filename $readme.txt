FIXME design - search for these, which designate request for external review
TODO major - designates significant unimplemented

9/20 intermittent failure in upd_order_reuse - perhaps ordering of rows in listener

    Failed run:
        @upd_order_reuse.py#<module>(): Reparenting *altered* order - new CustomerId: ANATR
        order amount 960.0000000000 projected to be 557.5000000000
        Logic Phase (sqlalchemy before_flush)			 - 2020-09-20 19:26:16,279 - logic_logger - DEBUG
        ..OrderDetail[1972] {Update - client} Amount: 530.0000000000, Discount: 0.05, Id: 1972, OrderId: 11011, ProductId:  [58-->] 48, Quantity:  [40-->] 10, ShippedDate: None, UnitPrice: 13.2500000000  row@: 0x105f620d0 - 2020-09-20 19:26:16,281 - logic_logger - DEBUG
        ..OrderDetail[1972] {copy_rules for role: ProductOrdered} Amount: 530.0000000000, Discount: 0.05, Id: 1972, OrderId: 11011, ProductId:  [58-->] 48, Quantity:  [40-->] 10, ShippedDate: None, UnitPrice: 13.2500000000  row@: 0x105f620d0 - 2020-09-20 19:26:16,282 - logic_logger - DEBUG
        ..OrderDetail[1972] {Formula Amount} Amount:  [530.0000000000-->] 127.5000000000, Discount: 0.05, Id: 1972, OrderId: 11011, ProductId:  [58-->] 48, Quantity:  [40-->] 10, ShippedDate: None, UnitPrice:  [13.2500000000-->] 12.7500000000  row@: 0x105f620d0 - 2020-09-20 19:26:16,289 - logic_logger - DEBUG
        ..OrderDetail[1972] {Prune Formula: ShippedDate [['OrderHeader.ShippedDate']]} Amount:  [530.0000000000-->] 127.5000000000, Discount: 0.05, Id: 1972, OrderId: 11011, ProductId:  [58-->] 48, Quantity:  [40-->] 10, ShippedDate: None, UnitPrice:  [13.2500000000-->] 12.7500000000  row@: 0x105f620d0 - 2020-09-20 19:26:16,290 - logic_logger - DEBUG
        ....Order[11011] {Update - Adjusting OrderHeader} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId: ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x105f4eb80 - 2020-09-20 19:26:16,291 - logic_logger - DEBUG
        ......Customer[ANATR] {Update - Adjusting Customer} Address: Avda. de la Constitución 2222, Balance:  [0E-10-->] -402.5000000000, City: México D.F., CompanyName: Ana Trujillo Emparedados y helados, ContactName: Ana Trujillo, ContactTitle: Owner, Country: Mexico, CreditLimit: 1000.0000000000, Fax: (5) 555-3745, Id: ANATR, Phone: (5) 555-4729, PostalCode: 05021, Region: Central America  row@: 0x105f7e880 - 2020-09-20 19:26:16,295 - logic_logger - DEBUG
                        ^
                        -- that's it... adjusting the new customer, works when orders go first (below)

        reparent order (upd_order_customer) worked...
        ..Order[11011] {Update - client} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId:  [ALFKI-->] ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x105f4eb80 - 2020-09-20 19:26:16,298 - logic_logger - DEBUG
        ....Customer[ANATR] {Update - Adjusting Customer} Address: Avda. de la Constitución 2222, Balance:  [-402.5000000000-->] 155.0000000000, City: México D.F., CompanyName: Ana Trujillo Emparedados y helados, ContactName: Ana Trujillo, ContactTitle: Owner, Country: Mexico, CreditLimit: 1000.0000000000, Fax: (5) 555-3745, Id: ANATR, Phone: (5) 555-4729, PostalCode: 05021, Region: Central America  row@: 0x105f7e880 - 2020-09-20 19:26:16,303 - logic_logger - DEBUG
        ....Customer[ALFKI] {Update - Adjusting Customer} Address: Obere Str. 57, Balance:  [960.0000000000-->] 0E-10, City: Berlin, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Country: Germany, CreditLimit: 2000.0000000000, Fax: 030-0076545, Id: ALFKI, Phone: 030-0074321, PostalCode: 12209, Region: Western Europe  row@: 0x105f7e5b0 - 2020-09-20 19:26:16,304 - logic_logger - DEBUG
        Commit Logic Phase   			 - 2020-09-20 19:26:16,305 - logic_logger - DEBUG
        ....Order[11011] {Commit Event} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId: ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x105f4eb80 - 2020-09-20 19:26:16,305 - logic_logger - DEBUG
        ....Order[11011] {Hi, Andrew, congratulate Janet on their new order} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId: ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x105f4eb80 - 2020-09-20 19:26:16,316 - logic_logger - DEBUG
        Flush Phase          			 - 2020-09-20 19:26:16,316 - logic_logger - DEBUG
        ..Order[11011] {Committed... order.amountTotal 960.0000000000 -> 557.5000000000} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId:  [ALFKI-->] ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x105f4eb80 - 2020-09-20 19:26:16,333 - logic_logger - DEBUG
        ..Customer[ALFKI] {Correct non-adjusted Customer Result} Address: Obere Str. 57, Balance:  [960.0000000000-->] 0E-10, City: Berlin, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Country: Germany, CreditLimit: 2000.0000000000, Fax: 030-0076545, Id: ALFKI, Phone: 030-0074321, PostalCode: 12209, Region: Western Europe  row@: 0x105f7e5b0 - 2020-09-20 19:26:16,336 - logic_logger - DEBUG
        *** ERROR***
        ..Customer[ANATR] {ERROR - incorrect adjusted Customer Result, should be 1362.50} Address: Avda. de la Constitución 2222, Balance:  [0E-10-->] 155.0000000000, City: México D.F., CompanyName: Ana Trujillo Emparedados y helados, ContactName: Ana Trujillo, ContactTitle: Owner, Country: Mexico, CreditLimit: 1000.0000000000, Fax: (5) 555-3745, Id: ANATR, Phone: (5) 555-4729, PostalCode: 05021, Region: Central America  row@: 0x105f7e880 - 2020-09-20 19:26:16,339 - logic_logger - DEBUG
        python-BaseException
        Traceback (most recent call last):
          File "/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pydev/pydevd.py", line 1448, in _exec
            pydev_imports.execfile(file, globals, locals)  # execute the script
          File "/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
            exec(compile(contents+"\n", file, 'exec'), glob, loc)
          File "/Users/val/python/pycharm/python-rules/nw/trans_tests/upd_order_reuse.py", line 136, in <module>
            assert False
        AssertionError

    Good run:
        @__init__.py#<module>(): session created, listeners registered

        ..Customer[ALFKI] {starting} Address: Obere Str. 57, Balance: 960.0000000000, City: Berlin, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Country: Germany, CreditLimit: 2000.0000000000, Fax: 030-0076545, Id: ALFKI, Phone: 030-0074321, PostalCode: 12209, Region: Western Europe  row@: 0x105074100 - 2020-09-20 19:36:30,581 - logic_logger - DEBUG
        ..Customer[ANATR] {starting} Address: Avda. de la Constitución 2222, Balance: 0E-10, City: México D.F., CompanyName: Ana Trujillo Emparedados y helados, ContactName: Ana Trujillo, ContactTitle: Owner, Country: Mexico, CreditLimit: 1000.0000000000, Fax: (5) 555-3745, Id: ANATR, Phone: (5) 555-4729, PostalCode: 05021, Region: Central America  row@: 0x105074970 - 2020-09-20 19:36:30,582 - logic_logger - DEBUG
        /Users/val/python/pycharm/python-rules/venv/lib/python3.8/site-packages/sqlalchemy/sql/sqltypes.py:661: SAWarning: Dialect sqlite+pysqlite does *not* support Decimal objects natively, and SQLAlchemy must convert from floating point - rounding errors and other issues may occur. Please consider storing Decimal numbers as strings or integers on this platform for lossless storage.
          util.warn(
        ..Order[11011] {starting} AmountTotal: 960.0000000000, CustomerId: ALFKI, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x1050bbb50 - 2020-09-20 19:36:30,590 - logic_logger - DEBUG


        @upd_order_reuse.py#<module>(): Reparenting *altered* order - new CustomerId: ANATR
        order amount 960.0000000000 projected to be 557.5000000000

        Logic Phase (sqlalchemy before_flush)			 - 2020-09-20 19:36:30,601 - logic_logger - DEBUG
        ..Order[11011] {Update - client} AmountTotal: 960.0000000000, CustomerId:  [ALFKI-->] ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x1050bbc40 - 2020-09-20 19:36:30,602 - logic_logger - DEBUG
        ....Customer[ANATR] {Update - Adjusting Customer} Address: Avda. de la Constitución 2222, Balance:  [0E-10-->] 960.0000000000, City: México D.F., CompanyName: Ana Trujillo Emparedados y helados, ContactName: Ana Trujillo, ContactTitle: Owner, Country: Mexico, CreditLimit: 1000.0000000000, Fax: (5) 555-3745, Id: ANATR, Phone: (5) 555-4729, PostalCode: 05021, Region: Central America  row@: 0x1050cf460 - 2020-09-20 19:36:30,611 - logic_logger - DEBUG
        ....Customer[ALFKI] {Update - Adjusting Customer} Address: Obere Str. 57, Balance:  [960.0000000000-->] 0E-10, City: Berlin, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Country: Germany, CreditLimit: 2000.0000000000, Fax: 030-0076545, Id: ALFKI, Phone: 030-0074321, PostalCode: 12209, Region: Western Europe  row@: 0x1050cfa00 - 2020-09-20 19:36:30,613 - logic_logger - DEBUG
        ..OrderDetail[1972] {Update - client} Amount: 530.0000000000, Discount: 0.05, Id: 1972, OrderId: 11011, ProductId:  [58-->] 48, Quantity:  [40-->] 10, ShippedDate: None, UnitPrice: 13.2500000000  row@: 0x1050cf190 - 2020-09-20 19:36:30,616 - logic_logger - DEBUG
        ..OrderDetail[1972] {copy_rules for role: ProductOrdered} Amount: 530.0000000000, Discount: 0.05, Id: 1972, OrderId: 11011, ProductId:  [58-->] 48, Quantity:  [40-->] 10, ShippedDate: None, UnitPrice: 13.2500000000  row@: 0x1050cf190 - 2020-09-20 19:36:30,616 - logic_logger - DEBUG
        ..OrderDetail[1972] {Formula Amount} Amount:  [530.0000000000-->] 127.5000000000, Discount: 0.05, Id: 1972, OrderId: 11011, ProductId:  [58-->] 48, Quantity:  [40-->] 10, ShippedDate: None, UnitPrice:  [13.2500000000-->] 12.7500000000  row@: 0x1050cf190 - 2020-09-20 19:36:30,623 - logic_logger - DEBUG
        ..OrderDetail[1972] {Prune Formula: ShippedDate [['OrderHeader.ShippedDate']]} Amount:  [530.0000000000-->] 127.5000000000, Discount: 0.05, Id: 1972, OrderId: 11011, ProductId:  [58-->] 48, Quantity:  [40-->] 10, ShippedDate: None, UnitPrice:  [13.2500000000-->] 12.7500000000  row@: 0x1050cf190 - 2020-09-20 19:36:30,623 - logic_logger - DEBUG
        ....Order[11011] {Update - Adjusting OrderHeader} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId: ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x1050bbc40 - 2020-09-20 19:36:30,625 - logic_logger - DEBUG
        ......Customer[ANATR] {Update - Adjusting Customer} Address: Avda. de la Constitución 2222, Balance:  [960.0000000000-->] 557.5000000000, City: México D.F., CompanyName: Ana Trujillo Emparedados y helados, ContactName: Ana Trujillo, ContactTitle: Owner, Country: Mexico, CreditLimit: 1000.0000000000, Fax: (5) 555-3745, Id: ANATR, Phone: (5) 555-4729, PostalCode: 05021, Region: Central America  row@: 0x1050cf460 - 2020-09-20 19:36:30,627 - logic_logger - DEBUG
        Commit Logic Phase   			 - 2020-09-20 19:36:30,628 - logic_logger - DEBUG
        ..Order[11011] {Commit Event} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId:  [ALFKI-->] ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x1050bbc40 - 2020-09-20 19:36:30,628 - logic_logger - DEBUG
        ..Order[11011] {Hi, Andrew, congratulate Janet on their new order} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId:  [ALFKI-->] ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x1050bbc40 - 2020-09-20 19:36:30,641 - logic_logger - DEBUG
        Flush Phase          			 - 2020-09-20 19:36:30,642 - logic_logger - DEBUG

        ..Order[11011] {Committed... order.amountTotal 960.0000000000 -> 557.5000000000} AmountTotal:  [960.0000000000-->] 557.5000000000, CustomerId:  [ALFKI-->] ANATR, EmployeeId: 3, Freight: 1.2100000000, Id: 11011, OrderDate: 2014-04-09, RequiredDate: 2014-05-07, ShipAddress: Obere Str. 57, ShipCity: Berlin, ShipCountry: Germany, ShipName: Alfred's Futterkiste, ShipPostalCode: 12209, ShipRegion: Western Europe, ShipVia: 1, ShippedDate: None  row@: 0x1050bbc40 - 2020-09-20 19:36:30,661 - logic_logger - DEBUG


        ..Customer[ALFKI] {Correct non-adjusted Customer Result} Address: Obere Str. 57, Balance:  [960.0000000000-->] 0E-10, City: Berlin, CompanyName: Alfreds Futterkiste, ContactName: Maria Anders, ContactTitle: Sales Representative, Country: Germany, CreditLimit: 2000.0000000000, Fax: 030-0076545, Id: ALFKI, Phone: 030-0074321, PostalCode: 12209, Region: Western Europe  row@: 0x1050cfa00 - 2020-09-20 19:36:30,666 - logic_logger - DEBUG
        ..Customer[ANATR] {Correct non-adjusted Customer Result} Address: Avda. de la Constitución 2222, Balance:  [0E-10-->] 557.5000000000, City: México D.F., CompanyName: Ana Trujillo Emparedados y helados, ContactName: Ana Trujillo, ContactTitle: Owner, Country: Mexico, CreditLimit: 1000.0000000000, Fax: (5) 555-3745, Id: ANATR, Phone: (5) 555-4729, PostalCode: 05021, Region: Central America  row@: 0x1050cf460 - 2020-09-20 19:36:30,669 - logic_logger - DEBUG

        upd_order_customer_reuse, ran to completion

        Process finished with exit code 0


Various misc copy/paste:

update orderdetail set amount = unitPrice * quantity

update "Order" set AmountTotal =
(select sum(orderdetail.amount) from orderdetail where orderdetail.orderid = "Order".id);

select id, customerid, shippeddate, amounttotal from "Order" where id = 11011;

select ProductName, UnitsInStock, UnitsShipped from Product where id = 58;

select id, balance, creditlimit from customer where id="ALFKI";
    960

update Customer set Balance =
(select sum("Order".amounttotal) from "Order" where Customer.id = "Order".customerid
and "Order".shippeddate is null);

update Customer set Balance = 0 where balance is null;
update Customer set Balance = 960  where id="ALFKI";

update Customer set creditlimit = balance + 100;

830 orders, 21 not shipped
    11045 for BOTTM (22607.7 ==> 1309.5)
    ALFKI has balance=0


select id, amounttotal from "Order" where id=11011;

CREATE TABLE IF NOT EXISTS "OrderX"
(
  "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "CustomerId" VARCHAR(8000) NULL,
  "EmployeeId" INTEGER NOT NULL,
  "OrderDate" VARCHAR(8000) NULL,
  "RequiredDate" VARCHAR(8000) NULL,
  "ShippedDate" VARCHAR(8000) NULL,
  "ShipVia" INTEGER NULL,
  "Freight" DECIMAL NOT NULL,
  "ShipName" VARCHAR(8000) NULL,
  "ShipAddress" VARCHAR(8000) NULL,
  "ShipCity" VARCHAR(8000) NULL,
  "ShipRegion" VARCHAR(8000) NULL,
  "ShipPostalCode" VARCHAR(8000) NULL,
  "ShipCountry" VARCHAR(8000) NULL, AmountTotal Decimal(10,2),
  FOREIGN KEY (CustomerId) REFERENCES Customer(Id),
  FOREIGN KEY (EmployeeId) REFERENCES Employee(Id)
);

insert into Orderx select * from "Order";
