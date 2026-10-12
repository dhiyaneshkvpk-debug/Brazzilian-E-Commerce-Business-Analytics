USE olist;
--DATA_VALIDATION
--A. Check_Total_Rows
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM order_items;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM seller;
SELECT COUNT(*) FROM order_payments;
SELECT COUNT(*) FROM order_reviews;
SELECT COUNT(*) FROM geolocation;
SELECT COUNT(*) FROM Product_catagory_name_translation;
--B. Checking_Table_Structure
DESCRIBE customers;
DESCRIBE orders;
DESCRIBE order_items;
DESCRIBE products;
DESCRIBE seller;
DESCRIBE order_payments;
DESCRIBE order_reviews;
DESCRIBE geolocation;
DESCRIBE Product_catagory_name_translation;
--C. Check_Duplicate_Primary_Keys
Select customer_id,
count(*) from customers
group by customer_id
Having count(*)>1;

Select customer_id,
count(*) from orders
group by customer_id
Having count(*)>1;
DESC orders;
--D.Check_Date_Columns
SELECT
MIN(order_purchase_timestamp),
MAX(order_purchase_timestamp)
FROM orders;
--E. Check_Numeric_Columns
SELECT
MIN(price),
MAX(price),
AVG(price)
FROM order_items;
--F. Checking_duplicate_customer_id
SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;
