USE olist;
--Business_analytics
--Total_revenue
SELECT
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items;
--TOTAL_FREIGHT_COST
SELECT
ROUND(SUM(freight_value), 2)
from order_items;
--Most_purchased_item
SELECT product_id, price, count(*) as total_orders
FROM order_items
GROUP BY product_id, price
ORDER BY Total_orders DESC
LIMIT 1;
--Total_number_of_orders
SELECT COUNT(*) as total_orders_placed
from orders;
--No_of_customer
SELECT COUNT(*) AS total_customers
FROM customers;
--Unique_customers_entry
SELECT COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;
--Numbers_of_cities_customers_from
SELECT COUNT(DISTINCT customer_city) AS Total_cities
from customers;
--Number_of_states_represented
SELECT COUNT(DISTINCT customer_state) AS Total_states
from customers;
--State_wise_customer_counts
SELECT customer_state,
count(*) AS Total_customers
FROM customers
GROUP BY Customer_state
ORDER BY total_customers DESC;
--City_with_hghest_number_of_customers
SELECT
	customer_city,
    Count(*) AS Total_customers
    FROM customers
    GROUP BY customer_city
ORDER BY total_customers DESC
LIMIT 10;
--State_with_least_number_of_customer
SELECT
    customer_state,
    COUNT(*) AS total_customers
FROM customers
GROUP BY customer_state
ORDER BY total_customers ASC
LIMIT 1;
--Cities--with_>_500_customers
SELECT
	customer_city,
    count(*) AS total_customers
FROM customers
GROUP BY customer_city
HAVING total_customers>500;
--Total_number_of_order_placed
SELECT COUNT(*) AS total_orders
FROM orders;
--different_order_status
SELECT DISTINCT order_status
from orders;
--Number_of_orders_in_each_status
SELECT
	order_status,
    COUNT(*) Total_orders
FROM orders
GROUP BY order_status
ORDER BY Total_orders
--Order_placed_each_year
SELECT
YEAR(order_purchase_timestamp) AS YEAR,
MONTH(order_purchase_timestamp) AS MONTH,
COUNT(*) AS Total_order
FROM orders
GROUP BY YEAR,MONTH
ORDER BY YEAR,MONTH
--Month_recorded_highest_number_of_orders
SELECT
MONTH(order_purchase_timestamp) AS MONTH,
COUNT(*) AS Total_orders
FROM orders
GROUP BY MONTH
ORDER BY Total_orders DESC
LIMIT 1;
--Day_of_the_week_most_orders_placed
SELECT
DAYNAME(order_purchase_timestamp) AS WEEKDAY,
COUNT(*) Total_orders
FROM orders
GROUP BY WEEKDAY
ORDER BY Total_orders DESC
LIMIT 1;
--Average_delivery_time
SELECT
ROUND(AVG(DATEDIFF(order_delivered_customer_date,
order_purchase_timestamp)),2) AS avg_delivery_days
FROM orders
WHERE order_status = "delivered"
--orders_were_delivered_on_or_before_the_estimated_delivery_date
SELECT
COUNT(*) AS on_time_orders
FROM orders
WHERE order_delivered_customer_date <= order_estimated_delivery_date;
--delayed_orders
SELECT
COUNT(*) AS delayed_order
FROM orders
WHERE order_delivered_customer_date > order_estimated_delivery_date;
Select*from products;
--Total_number_of_products
SELECT
COUNT(*) AS total_products
FROM products;
--Number_of_Unique_product_category
SELECT
COUNT(DISTINCT Product_category_name) as Total_category
FROM Products;
--Most_products_having_category
SELECT
	Product_category_name,
	COUNT(*) AS total_products
FROM Products
GROUP BY Product_category_name
ORDER BY Total_products DESC
LIMIT 10;
--least_products_having_category
SELECT
	Product_category_name,
	COUNT(*) AS total_products
FROM Products
GROUP BY Product_category_name
ORDER BY Total_products ASC
LIMIT 10;
--lightest_and_heaviest_products
SELECT
MAX(PRODUCT_weight_g) AS MAX_WEIGHT,
MIN(PRODUCT_weight_g) AS MIN_WEIGHT
FROM Products;
--products have the largest volume
SELECT
product_id,
(product_length_cm * product_width_cm * product_height_cm) AS volume_cm3
FROM products
WHERE product_length_cm IS NOT NULL
AND product_width_cm IS NOT NULL
AND product_height_cm IS NOT NULL
ORDER BY volume_cm3 DESC
LIMIT 10;
--categories contain more_than_1000_products
SELECT
product_category_name,
COUNT(*) AS total_products
FROM products
GROUP BY product_category_name
HAVING COUNT(*) > 1000
ORDER BY total_products DESC;
--average_selling_price_of_product
SELECT
ROUND(AVG(price),2) AS average_product_price
FROM order_items;
--products generate the highest revenue
SELECT
	product_id,
	ROUND(SUM(price),2) AS revenue
FROM Order_items
group by Product_id
ORDER BY Revenue DESC
LIMIT 10;
--Most sold products
SELECT
product_id,
COUNT(*) AS units_sold
FROM order_items
GROUP BY product_id
ORDER BY units_sold DESC
LIMIT 10;
--sellers sold the most items
SELECT
seller_id,
COUNT(*) AS total_items_sold
FROM order_items
GROUP BY seller_id
ORDER BY total_items_sold DESC
LIMIT 10;
--total payment received
SELECT
ROUND(SUM(payment_value),2) AS total_payment
FROM order_payments;
--total revenue by payment method
SELECT
payment_type,
ROUND(SUM(payment_value),2) AS revenue
FROM order_payments
GROUP BY payment_type
ORDER BY revenue DESC;
--installments_customers usually choose
SELECT
payment_installments,
COUNT(*) AS total_orders
FROM order_payments
GROUP BY payment_installments
ORDER BY total_orders DESC;
--average review score
SELECT
ROUND(AVG(review_score),2) AS average_rating
FROM order_reviews;
--review scores distributed
SELECT
review_score,
COUNT(*) AS total_reviews
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;
--received_5-star reviews
SELECT
COUNT(*) AS five_star_reviews
FROM order_reviews
WHERE review_score=5;
--received_1_star review
SELECT
COUNT(*) AS one_star_reviews
FROM order_reviews
WHERE review_score=1;
SELECT
COUNT(*) AS total_sellers
FROM sellers;
--states have sellers
SELECT
COUNT(DISTINCT seller_state) AS total_states
FROM seller;
--states have the most sellers
SELECT
seller_state,
COUNT(*) AS total_sellers
FROM seller
GROUP BY seller_state
ORDER BY total_sellers DESC;
--states have the least sellers
SELECT
seller_state,
COUNT(*) AS total_sellers
FROM seller
GROUP BY seller_state
ORDER BY total_sellers DESC;
--cities have the most sellers
SELECT
seller_city,
COUNT(*) AS total_sellers
FROM seller
GROUP BY seller_city
ORDER BY total_sellers DESC
LIMIT 10;
--geolocation records
SELECT
COUNT(*) AS total_locations
FROM geolocation;
--unique cities exist
SELECT
COUNT(DISTINCT geolocation_city) AS total_cities
FROM geolocation;
--unique states exist
SELECT
COUNT(DISTINCT geolocation_state) AS total_states
FROM geolocation;
--cities have the most location records
SELECT
geolocation_city,
COUNT(*) AS total_records
FROM geolocation
GROUP BY geolocation_city
ORDER BY total_records DESC
LIMIT 10;
--List_all product categories
SELECT
product_category_name,
product_category_name_english
FROM product_catagory_name_translation
ORDER BY product_category_name_english;
show tables;
--Finding categories starting with "c"
SELECT
product_category_name_english
FROM product_catagory_name_translation
WHERE product_category_name_english LIKE 'c%';
--states have placed the highest number_of_orders
SELECT
    c.customer_state,
    COUNT(o.order_id) AS total_orders
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_state
ORDER BY total_orders DESC;
--customers have placed the most orders
SELECT
    c.customer_unique_id,
    COUNT(o.order_id) AS total_orders
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
ORDER BY total_orders DESC
LIMIT 10;
--sellers generate the highest revenue
SELECT
    s.seller_id,
    ROUND(SUM(oi.price),2) AS total_revenue
FROM seller s
INNER JOIN order_items oi
    ON s.seller_id = oi.seller_id
GROUP BY s.seller_id
ORDER BY total_revenue DESC
LIMIT 10;
--product categories have the most products
SELECT
    pct.product_category_name_english,
    COUNT(*) AS total_products
FROM products p
INNER JOIN product_catagory_name_translation pct
    ON p.product_category_name = pct.product_category_name
GROUP BY pct.product_category_name_english
ORDER BY total_products DESC
LIMIT 10;
--payment method used the most
SELECT
    op.payment_type,
    COUNT(*) AS total_transactions
FROM orders o
INNER JOIN order_payments op
    ON o.order_id = op.order_id
GROUP BY op.payment_type
ORDER BY total_transactions DESC;
--Rank Sellers-Revenue
SELECT
    seller_id,
    ROUND(SUM(price),2) AS revenue,
    RANK() OVER(
        ORDER BY SUM(price) DESC
    ) AS seller_rank
FROM order_items
GROUP BY seller_id;
--Row_Number_for_Customers
SELECT
    customer_unique_id,
    customer_state,
    ROW_NUMBER() OVER(
        ORDER BY customer_unique_id
    ) AS row_num
FROM customers;
--Dense_Rank_of_Product Categories
SELECT
    product_category_name,
    COUNT(*) AS total_products,
    DENSE_RANK() OVER(
        ORDER BY COUNT(*) DESC
    ) AS category_rank
FROM products
GROUP BY product_category_name;