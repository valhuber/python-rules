FIXME design - search for these, which designate request for external review
TODO major - designates significant unimplemented


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
