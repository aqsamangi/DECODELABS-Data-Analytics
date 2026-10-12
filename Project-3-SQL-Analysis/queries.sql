-- =====================================================================
-- PROJECT 3 - SQL DATA ANALYSIS
-- DecodeLabs Internship - Week 3
-- Database: orders.db | Table: orders
-- =====================================================================
-- Run these queries with DB Browser for SQLite (or any SQLite tool)
-- after creating orders.db with load_to_sqlite.py
-- =====================================================================


-- ---------------------------------------------------------------
-- 1. SELECT - view the whole table
-- ---------------------------------------------------------------
-- Shows every column, for the first 10 rows only, so you can see
-- what the table looks like without printing all 1,200 rows.
SELECT *
FROM orders
LIMIT 10;


-- ---------------------------------------------------------------
-- 2. SELECT specific columns
-- ---------------------------------------------------------------
-- Instead of every column, pick only the ones relevant to a question:
-- "What did customers order, and what did they pay?"
SELECT OrderID, Product, Quantity, TotalPrice
FROM orders
LIMIT 10;


-- ---------------------------------------------------------------
-- 3. DISTINCT - list unique values
-- ---------------------------------------------------------------
-- Shows each product name ONCE, even though many orders share the
-- same product. Useful for seeing "what categories exist?"
SELECT DISTINCT Product
FROM orders;


-- ---------------------------------------------------------------
-- 4. DISTINCT on two columns together
-- ---------------------------------------------------------------
-- Shows every unique combination of payment method and order status
-- that actually occurs in the data.
SELECT DISTINCT PaymentMethod, OrderStatus
FROM orders;


-- ---------------------------------------------------------------
-- 5. WHERE - filter rows by a condition
-- ---------------------------------------------------------------
-- Only shows orders that were Cancelled.
SELECT OrderID, Product, OrderStatus, TotalPrice
FROM orders
WHERE OrderStatus = 'Cancelled';


-- ---------------------------------------------------------------
-- 6. WHERE with a number comparison
-- ---------------------------------------------------------------
-- Only shows "big" orders - those worth more than $2,000.
SELECT OrderID, Product, TotalPrice
FROM orders
WHERE TotalPrice > 2000;


-- ---------------------------------------------------------------
-- 7. WHERE with AND (two conditions must both be true)
-- ---------------------------------------------------------------
-- Orders that were Delivered AND paid by Credit Card.
SELECT OrderID, Product, PaymentMethod, OrderStatus
FROM orders
WHERE OrderStatus = 'Delivered' AND PaymentMethod = 'Credit Card';


-- ---------------------------------------------------------------
-- 8. WHERE with IN (matches any value in a list)
-- ---------------------------------------------------------------
-- Orders for either a Laptop or a Phone.
SELECT OrderID, Product, TotalPrice
FROM orders
WHERE Product IN ('Laptop', 'Phone');


-- ---------------------------------------------------------------
-- 9. ORDER BY - sort results
-- ---------------------------------------------------------------
-- Shows the 10 highest-value orders first (DESC = largest to smallest).
SELECT OrderID, Product, TotalPrice
FROM orders
ORDER BY TotalPrice DESC
LIMIT 10;


-- ---------------------------------------------------------------
-- 10. ORDER BY ascending (smallest first)
-- ---------------------------------------------------------------
-- Shows the 10 cheapest orders.
SELECT OrderID, Product, TotalPrice
FROM orders
ORDER BY TotalPrice ASC
LIMIT 10;


-- ---------------------------------------------------------------
-- 11. COUNT - how many rows total?
-- ---------------------------------------------------------------
SELECT COUNT(*) AS TotalOrders
FROM orders;


-- ---------------------------------------------------------------
-- 12. COUNT with WHERE
-- ---------------------------------------------------------------
-- How many orders were Returned?
SELECT COUNT(*) AS ReturnedOrders
FROM orders
WHERE OrderStatus = 'Returned';


-- ---------------------------------------------------------------
-- 13. GROUP BY + COUNT - frequency count per category
-- ---------------------------------------------------------------
-- How many orders exist for each product?
SELECT Product, COUNT(*) AS NumberOfOrders
FROM orders
GROUP BY Product
ORDER BY NumberOfOrders DESC;


-- ---------------------------------------------------------------
-- 14. GROUP BY + SUM - total revenue per category
-- ---------------------------------------------------------------
-- Which product earns the most total revenue?
SELECT Product, SUM(TotalPrice) AS TotalRevenue
FROM orders
GROUP BY Product
ORDER BY TotalRevenue DESC;


-- ---------------------------------------------------------------
-- 15. GROUP BY + AVG - average order value per category
-- ---------------------------------------------------------------
-- What is the average amount spent per payment method?
SELECT PaymentMethod, AVG(TotalPrice) AS AvgOrderValue
FROM orders
GROUP BY PaymentMethod
ORDER BY AvgOrderValue DESC;


-- ---------------------------------------------------------------
-- 16. GROUP BY + MIN/MAX - smallest and largest order per category
-- ---------------------------------------------------------------
SELECT Product,
       MIN(TotalPrice) AS CheapestOrder,
       MAX(TotalPrice) AS MostExpensiveOrder
FROM orders
GROUP BY Product;


-- ---------------------------------------------------------------
-- 17. GROUP BY on OrderStatus - full breakdown
-- ---------------------------------------------------------------
SELECT OrderStatus,
       COUNT(*) AS NumberOfOrders,
       SUM(TotalPrice) AS TotalRevenue,
       AVG(TotalPrice) AS AvgOrderValue
FROM orders
GROUP BY OrderStatus
ORDER BY NumberOfOrders DESC;


-- ---------------------------------------------------------------
-- 18. HAVING - filter GROUPED results (not individual rows)
-- ---------------------------------------------------------------
-- WHERE filters rows BEFORE grouping; HAVING filters AFTER grouping.
-- This shows only referral sources that brought in more than 240 orders.
SELECT ReferralSource, COUNT(*) AS NumberOfOrders
FROM orders
GROUP BY ReferralSource
HAVING COUNT(*) > 240
ORDER BY NumberOfOrders DESC;


-- ---------------------------------------------------------------
-- 19. HAVING with an aggregate condition (average)
-- ---------------------------------------------------------------
-- Which products have an average order value above $350?
SELECT Product, AVG(TotalPrice) AS AvgOrderValue
FROM orders
GROUP BY Product
HAVING AVG(TotalPrice) > 350
ORDER BY AvgOrderValue DESC;


-- ---------------------------------------------------------------
-- 20. Combining WHERE + GROUP BY + HAVING + ORDER BY + LIMIT
-- ---------------------------------------------------------------
-- Among DELIVERED orders only, which products earned over $20,000
-- in total revenue? Show the top 3.
SELECT Product, SUM(TotalPrice) AS TotalRevenue
FROM orders
WHERE OrderStatus = 'Delivered'
GROUP BY Product
HAVING SUM(TotalPrice) > 20000
ORDER BY TotalRevenue DESC
LIMIT 3;


-- ---------------------------------------------------------------
-- 21. Overall summary statistics in one query
-- ---------------------------------------------------------------
SELECT
    COUNT(*)          AS TotalOrders,
    SUM(TotalPrice)   AS TotalRevenue,
    AVG(TotalPrice)   AS AvgOrderValue,
    MIN(TotalPrice)   AS SmallestOrder,
    MAX(TotalPrice)   AS LargestOrder
FROM orders;
