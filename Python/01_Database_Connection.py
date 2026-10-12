# =============================================================
# IMPORT LIBRARIES
# =============================================================

import pandas as pd
import numpy as np
import pymysql as ps
import warnings

# Ignore unnecessary warnings
warnings.filterwarnings("ignore", category=UserWarning)


# =============================================================
# CONNECT TO MYSQL DATABASE
# =============================================================

connection = ps.connect(
    host="localhost",
    user="root",
    password="Yash@619",
    database="olist"
)

print(connection)


# =============================================================
# LOAD TABLES
# =============================================================

print("\n========================== OLIST TABLES ==========================")


def load_table(table_name):

    query = f"SELECT * FROM {table_name};"

    return pd.read_sql(query, connection)


customers = load_table("customers")
orders = load_table("orders")
products = load_table("products")
seller = load_table("seller")
order_items = load_table("order_items")
order_payments = load_table("order_payments")
order_reviews = load_table("order_reviews")
geolocation = load_table("geolocation")
translation = load_table(
    "product_catagory_name_translation"
)


# =============================================================
# CHECK TABLE SHAPES
# =============================================================

print("\n========================== TABLE SHAPES ==========================")

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Products:", products.shape)
print("Seller:", seller.shape)
print("Order Items:", order_items.shape)
print("Order Payments:", order_payments.shape)
print("Order Reviews:", order_reviews.shape)
print("Geolocation:", geolocation.shape)
print("Translation:", translation.shape)


# =============================================================
# CHECK FIRST 5 ROWS
# =============================================================

print("\n========================== FIRST 5 ROWS ==========================")

print("\nCustomers:")
print(customers.head())

print("\nOrders:")
print(orders.head())

print("\nProducts:")
print(products.head())

print("\nSeller:")
print(seller.head())

print("\nOrder Items:")
print(order_items.head())

print("\nOrder Payments:")
print(order_payments.head())

print("\nOrder Reviews:")
print(order_reviews.head())

print("\nGeolocation:")
print(geolocation.head())

print("\nTranslation:")
print(translation.head())


# =============================================================
# CHECK DATA TYPES
# =============================================================

print("\n========================== DATA TYPES ==========================")

print("\nCustomers:")
print(customers.dtypes)

print("\nOrders:")
print(orders.dtypes)

print("\nProducts:")
print(products.dtypes)

print("\nOrder Items:")
print(order_items.dtypes)

print("\nOrder Payments:")
print(order_payments.dtypes)

print("\nOrder Reviews:")
print(order_reviews.dtypes)


# =============================================================
# STORE ALL TABLES IN ONE DICTIONARY
# =============================================================

tables = {

    "Customers": customers,
    "Orders": orders,
    "Products": products,
    "Seller": seller,
    "Order Items": order_items,
    "Payments": order_payments,
    "Reviews": order_reviews,
    "Geolocation": geolocation,
    "Translation": translation

}


# =============================================================
# CLOSE DATABASE CONNECTION
# =============================================================

connection.close()

print("\nDatabase connection closed.")


# =============================================================
# DATA CLEANING
# =============================================================

print("\n========================== DATA CLEANING ==========================")


# -------------------------------------------------------------
# 1. CONVERT BLANK STRINGS TO NaN
# -------------------------------------------------------------

print("\nConverting blank strings to NaN...")

for name, df in tables.items():

    df.replace(
        r"^\s*$",
        np.nan,
        regex=True,
        inplace=True
    )

print("Blank strings converted to NaN.")


# =============================================================
# 2. PRODUCT MEASUREMENT CLEANING
# =============================================================

print("\n========================== PRODUCT CLEANING ==========================")


measurement_columns = [

    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"

]


# -------------------------------------------------------------
# CHECK ZERO VALUES BEFORE CLEANING
# -------------------------------------------------------------

print("\nZero values before cleaning:")

print(
    products[measurement_columns]
    .eq(0)
    .sum()
)


# -------------------------------------------------------------
# CONVERT ZERO TO NaN
# -------------------------------------------------------------

for col in measurement_columns:

    products[col] = products[col].replace(
        0,
        np.nan
    )


# -------------------------------------------------------------
# CHECK MISSING VALUES AFTER CLEANING
# -------------------------------------------------------------

print("\nMissing product measurements after cleaning:")

print(
    products[measurement_columns]
    .isna()
    .sum()
)


# =============================================================
# 3. CHECK MISSING VALUES IN ALL TABLES
# =============================================================

print("\n========================== MISSING VALUES ==========================")


for name, df in tables.items():

    print(f"\n===== {name} =====")

    missing = df.isna().sum()

    missing = missing[missing > 0]

    if missing.empty:

        print("No missing values")

    else:

        print(missing)


# =============================================================
# 4. PRODUCT MISSING VALUE ANALYSIS
# =============================================================

print("\n========================== PRODUCT MISSING VALUES ==========================")


product_missing = products[
    products["product_category_name"].isna()
]


print(
    "Products missing category:",
    len(product_missing)
)


product_columns = [

    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty"

]


print("\nMissing values in product columns:")

print(
    products[product_columns]
    .isna()
    .sum()
)


# =============================================================
# 5. PRODUCT MISSING VALUE PERCENTAGE
# =============================================================

print("\n========================== PRODUCT MISSING VALUE SUMMARY ==========================")


product_missing_report = pd.DataFrame({

    "Missing_Count":
        products.isna().sum(),

    "Missing_Percentage":
        (
            products.isna().mean() * 100
        ).round(2)

})


product_missing_report = product_missing_report[
    product_missing_report["Missing_Count"] > 0
]


print(product_missing_report)


# =============================================================
# 6. REVIEW MISSING VALUE ANALYSIS
# =============================================================

print("\n========================== REVIEW MISSING VALUES ==========================")


reviews_without_comments = order_reviews[
    order_reviews["review_comment_title"].isna() &
    order_reviews["review_comment_message"].isna()
]


print(
    "Reviews without title and message:",
    len(reviews_without_comments)
)


percentage_without_comment = (

    len(reviews_without_comments)
    /
    len(order_reviews)
    *
    100

)


print(
    "Percentage of reviews without comments:",
    round(percentage_without_comment, 2),
    "%"
)


# -------------------------------------------------------------
# CREATE REVIEW COMMENT FLAG
# -------------------------------------------------------------

order_reviews["has_comment"] = np.where(

    order_reviews["review_comment_message"].notna(),

    1,

    0

)


print("\nReview comment status:")

print(
    order_reviews["has_comment"]
    .value_counts()
)


# =============================================================
# 7. ORDERS DATE CLEANING
# =============================================================

print("\n========================== ORDER DATE CLEANING ==========================")


order_date_columns = [

    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"

]


# -------------------------------------------------------------
# CONVERT DATE COLUMNS
# -------------------------------------------------------------

for col in order_date_columns:

    orders[col] = pd.to_datetime(

        orders[col],

        errors="coerce"

    )


print("\nOrder date data types:")

print(
    orders[order_date_columns]
    .dtypes
)


# =============================================================
# 8. CHECK MISSING ORDER DATES
# =============================================================

print("\n========================== MISSING ORDER DATES ==========================")


print(
    orders[order_date_columns]
    .isna()
    .sum()
)


# =============================================================
# 9. ORDER STATUS
# =============================================================

print("\n========================== ORDER STATUS ==========================")


print(
    orders["order_status"]
    .value_counts()
)


# =============================================================
# 10. MISSING DATES BY ORDER STATUS
# =============================================================

print("\n========================== MISSING DATES BY STATUS ==========================")


print("\nMissing approval date:")

print(

    orders[
        orders["order_approved_at"].isna()
    ]["order_status"]
    .value_counts()

)


print("\nMissing carrier date:")

print(

    orders[
        orders["order_delivered_carrier_date"].isna()
    ]["order_status"]
    .value_counts()

)


print("\nMissing customer delivery date:")

print(

    orders[
        orders["order_delivered_customer_date"].isna()
    ]["order_status"]
    .value_counts()

)


# =============================================================
# 11. DELIVERED ORDERS WITH MISSING DELIVERY DATE
# =============================================================

print("\n========================== DELIVERED ORDERS WITHOUT DELIVERY DATE ==========================")


delivered_missing_delivery = orders[

    (orders["order_status"] == "delivered")

    &

    (orders["order_delivered_customer_date"].isna())

]


print(

    "Delivered orders without delivery date:",

    len(delivered_missing_delivery)

)


# =============================================================
# 12. DELIVERED ORDERS WITH MISSING CARRIER DATE
# =============================================================

print("\n========================== DELIVERED ORDERS WITHOUT CARRIER DATE ==========================")


delivered_missing_carrier = orders[

    (orders["order_status"] == "delivered")

    &

    (orders["order_delivered_carrier_date"].isna())

]
print(
    "Delivered orders without carrier date:",
    len(delivered_missing_carrier)
)
# =============================================================
# 13. DELIVERED ORDERS WITH MISSING APPROVAL DATE
# =============================================================

print("\n========================== DELIVERED ORDERS WITHOUT APPROVAL DATE ==========================")


delivered_missing_approval = orders[

    (orders["order_status"] == "delivered")

    &

    (orders["order_approved_at"].isna())

]


print(

    "Delivered orders without approval date:",

    len(delivered_missing_approval)

)


# =============================================================
# 14. BASIC DATE LOGIC CHECK
# =============================================================

print("\n========================== DATE LOGIC CHECK ==========================")


# Approval should not happen before purchase

invalid_approval = orders[

    orders["order_approved_at"].notna()

    &

    orders["order_purchase_timestamp"].notna()

    &

    (
        orders["order_approved_at"]
        <
        orders["order_purchase_timestamp"]
    )

]


print(

    "Approval before purchase:",

    len(invalid_approval)

)


# Carrier should normally come after approval

invalid_carrier = orders[

    orders["order_delivered_carrier_date"].notna()

    &

    orders["order_approved_at"].notna()

    &

    (
        orders["order_delivered_carrier_date"]
        <
        orders["order_approved_at"]
    )

]


print(

    "Carrier before approval:",

    len(invalid_carrier)

)


# Customer delivery should normally come after carrier

invalid_delivery = orders[

    orders["order_delivered_customer_date"].notna()

    &

    orders["order_delivered_carrier_date"].notna()

    &

    (
        orders["order_delivered_customer_date"]
        <
        orders["order_delivered_carrier_date"]
    )

]


print(

    "Delivery before carrier:",

    len(invalid_delivery)

)


# =============================================================
# 15. CREATE VALID DELIVERY DATASET
# =============================================================

print("\n========================== DELIVERY ANALYSIS ==========================")


valid_delivery = orders[

    (orders["order_status"] == "delivered")

    &

    (orders["order_purchase_timestamp"].notna())

    &

    (orders["order_delivered_customer_date"].notna())

].copy()


# =============================================================
# 16. CALCULATE DELIVERY DAYS
# =============================================================

valid_delivery["delivery_days"] = (

    valid_delivery["order_delivered_customer_date"]

    -

    valid_delivery["order_purchase_timestamp"]

).dt.total_seconds() / (60 * 60 * 24)


print("\nDelivery time summary:")

print(
    valid_delivery["delivery_days"]
    .describe()
)


# =============================================================
# 17. ESTIMATED VS ACTUAL DELIVERY
# =============================================================

valid_delivery["delivery_delay_days"] = (

    valid_delivery["order_delivered_customer_date"]

    -

    valid_delivery["order_estimated_delivery_date"]

).dt.total_seconds() / (60 * 60 * 24)


print("\n========================== DELIVERY DELAY ==========================")


print(
    valid_delivery["delivery_delay_days"]
    .describe()
)


# =============================================================
# 18. LATE DELIVERY FLAG
# =============================================================

valid_delivery["late_delivery"] = np.where(

    valid_delivery["delivery_delay_days"] > 0,

    1,

    0

)


print("\nLate delivery summary:")

print(

    valid_delivery["late_delivery"]
    .value_counts()

)


# =============================================================
# 19. LONGEST DELIVERIES
# =============================================================

print("\n========================== LONGEST DELIVERIES ==========================")


longest_deliveries = (

    valid_delivery[

        [
            "order_id",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "delivery_days"
        ]

    ]

    .sort_values(

        "delivery_days",

        ascending=False

    )

    .head(10)

)


print(longest_deliveries)


# =============================================================
# 20. DELIVERY OUTLIER CHECK
# =============================================================

print("\n========================== DELIVERY OUTLIER CHECK ==========================")


print(

    "Orders delivered in more than 30 days:",

    (
        valid_delivery["delivery_days"] > 30
    ).sum()

)


print(

    "Orders delivered in more than 60 days:",

    (
        valid_delivery["delivery_days"] > 60
    ).sum()

)


print(

    "Orders delivered in more than 90 days:",

    (
        valid_delivery["delivery_days"] > 90
    ).sum()

)


# =============================================================
# 21. FINAL DATA QUALITY CHECK
# =============================================================

print("\n========================== FINAL DATA QUALITY CHECK ==========================")


for name, df in tables.items():

    total_missing = df.isna().sum().sum()

    print(

        f"{name}:",

        total_missing,

        "missing values"

    )


# =============================================================
# 22. FINAL TABLE SHAPES
# =============================================================

print("\n========================== FINAL TABLE SHAPES ==========================")


for name, df in tables.items():

    print(

        f"{name}:",

        df.shape

    )
print("\n========================== DATA CLEANING COMPLETED ==========================")
# ============================================================
# FEATURE ENGINEERING
# ============================================================

print("\n========================== FEATURE ENGINEERING ==========================")


# ============================================================
# 1. ORDER PURCHASE DATE FEATURES
# ============================================================

orders["purchase_year"] = (
    orders["order_purchase_timestamp"].dt.year
)

orders["purchase_month"] = (
    orders["order_purchase_timestamp"].dt.month
)

orders["purchase_day"] = (
    orders["order_purchase_timestamp"].dt.day
)

orders["purchase_day_name"] = (
    orders["order_purchase_timestamp"].dt.day_name()
)

orders["purchase_month_name"] = (
    orders["order_purchase_timestamp"].dt.month_name()
)


# ============================================================
# 2. PURCHASE HOUR
# ============================================================

orders["purchase_hour"] = (
    orders["order_purchase_timestamp"].dt.hour
)


# ============================================================
# 3. WEEKEND FLAG
# ============================================================

orders["is_weekend"] = np.where(
    orders["order_purchase_timestamp"].dt.dayofweek >= 5,
    1,
    0
)


# ============================================================
# 4. DELIVERY DAYS
# ============================================================

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    -
    orders["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60 * 24)


# ============================================================
# 5. ESTIMATED DELIVERY DELAY
# ============================================================

orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    -
    orders["order_estimated_delivery_date"]
).dt.total_seconds() / (60 * 60 * 24)


# ============================================================
# 6. LATE DELIVERY FLAG
# ============================================================

orders["late_delivery"] = np.where(
    orders["delivery_delay_days"] > 0,
    1,
    0
)


# ============================================================
# 7. EARLY / ON-TIME DELIVERY FLAG
# ============================================================

orders["on_time_delivery"] = np.where(
    orders["delivery_delay_days"] <= 0,
    1,
    0
)


# ============================================================
# CHECK NEW FEATURES
# ============================================================

print("\nNew columns in Orders:")

print(
    orders[
        [
            "order_id",
            "order_status",
            "purchase_year",
            "purchase_month",
            "purchase_day_name",
            "purchase_hour",
            "is_weekend",
            "delivery_days",
            "delivery_delay_days",
            "late_delivery",
            "on_time_delivery"
        ]
    ].head(10)
)
# ============================================================
# BASIC BUSINESS METRICS
# ============================================================

print("\n========================== BASIC BUSINESS METRICS ==========================")


# Total orders

total_orders = orders["order_id"].nunique()

print(
    "Total Orders:",
    total_orders
)


# ============================================================
# ORDER STATUS
# ============================================================

print("\nOrder Status:")

print(
    orders["order_status"]
    .value_counts()
)


# ============================================================
# DELIVERED ORDERS
# ============================================================

delivered_orders = (
    orders["order_status"] == "delivered"
).sum()

print(
    "\nDelivered Orders:",
    delivered_orders
)


# ============================================================
# CANCELLED ORDERS
# ============================================================

cancelled_orders = (
    orders["order_status"] == "canceled"
).sum()

print(
    "Cancelled Orders:",
    cancelled_orders
)


# ============================================================
# DELIVERY RATE
# ============================================================

delivery_rate = (
    delivered_orders /
    total_orders *
    100
)

print(
    "Delivery Rate:",
    round(delivery_rate, 2),
    "%"
)


# ============================================================
# CANCELLATION RATE
# ============================================================

cancellation_rate = (
    cancelled_orders /
    total_orders *
    100
)

print(
    "Cancellation Rate:",
    round(cancellation_rate, 2),
    "%"
)
# ============================================================
# ORDER ITEMS ANALYSIS
# ============================================================

print("\n========================== ORDER ITEMS ANALYSIS ==========================")


# ============================================================
# 1. MISSING VALUES
# ============================================================

print("\nMissing values:")

print(
    order_items.isna().sum()
)


# ============================================================
# 2. DUPLICATES
# ============================================================

print("\nDuplicate rows:")

print(
    order_items.duplicated().sum()
)


# ============================================================
# 3. PRICE SUMMARY
# ============================================================

print("\nPrice Summary:")

print(
    order_items["price"].describe()
)


# ============================================================
# 4. FREIGHT VALUE SUMMARY
# ============================================================

print("\nFreight Value Summary:")

print(
    order_items["freight_value"].describe()
)


# ============================================================
# 5. CHECK ZERO PRICE
# ============================================================

print("\nZero price records:")

print(
    (order_items["price"] == 0).sum()
)


# ============================================================
# 6. CHECK ZERO FREIGHT
# ============================================================

print("\nZero freight records:")

print(
    (order_items["freight_value"] == 0).sum()
)
# ============================================================
# PAYMENTS ANALYSIS
# ============================================================

print("\n========================== PAYMENTS ANALYSIS ==========================")


print("\nMissing values:")

print(
    order_payments.isna().sum()
)


print("\nPayment types:")

print(
    order_payments["payment_type"]
    .value_counts()
)


print("\nPayment installments:")

print(
    order_payments["payment_installments"]
    .value_counts()
)


print("\nPayment value summary:")

print(
    order_payments["payment_value"]
    .describe()
)
# ============================================================
# PAYMENT VALUE BY PAYMENT TYPE
# ============================================================

payment_summary = (
    order_payments
    .groupby("payment_type")["payment_value"]
    .agg(["count", "sum", "mean"])
    .sort_values(
        "sum",
        ascending=False
    )
)

print("\nPayment Summary:")

print(payment_summary)
# ============================================================
# REVIEWS ANALYSIS
# ============================================================

print("\n========================== REVIEWS ANALYSIS ==========================")


print("\nReview Score Distribution:")

print(
    order_reviews["review_score"]
    .value_counts()
    .sort_index()
)


print("\nAverage Review Score:")

print(
    order_reviews["review_score"].mean()
)


print("\nReview Score Summary:")

print(
    order_reviews["review_score"].describe()
)
# ============================================================
# REVIEWS ANALYSIS
# ============================================================

print("\n========================== REVIEWS ANALYSIS ==========================")


print("\nReview Score Distribution:")

print(
    order_reviews["review_score"]
    .value_counts()
    .sort_index()
)


print("\nAverage Review Score:")

print(
    order_reviews["review_score"].mean()
)


print("\nReview Score Summary:")

print(
    order_reviews["review_score"].describe()
)
# =============================================================
# RELATIONSHIP CHECK
# =============================================================

print("\n========================== RELATIONSHIP CHECK ==========================")


# -------------------------------------------------------------
# 1. ORDERS → CUSTOMERS
# -------------------------------------------------------------

customer_check = orders[
    ~orders["customer_id"].isin(
        customers["Customer_id"]
    )
]

print(
    "Orders without matching customer:",
    len(customer_check)
)


# -------------------------------------------------------------
# 2. ORDER ITEMS → ORDERS
# -------------------------------------------------------------

order_check = order_items[
    ~order_items["order_id"].isin(
        orders["order_id"]
    )
]

print(
    "Order items without matching order:",
    len(order_check)
)


# -------------------------------------------------------------
# 3. ORDER ITEMS → PRODUCTS
# -------------------------------------------------------------

product_check = order_items[
    ~order_items["product_id"].isin(
        products["product_id"]
    )
]

print(
    "Order items without matching product:",
    len(product_check)
)


# -------------------------------------------------------------
# 4. ORDER ITEMS → SELLERS
# -------------------------------------------------------------

seller_check = order_items[
    ~order_items["seller_id"].isin(
        seller["seller_id"]
    )
]

print(
    "Order items without matching seller:",
    len(seller_check)
)


# =============================================================
# RELATIONSHIP CHECK SUMMARY
# =============================================================

print("\n========================== RELATIONSHIP CHECK SUMMARY ==========================")

print(
    "Customer relationship valid:",
    len(customer_check) == 0
)

print(
    "Order relationship valid:",
    len(order_check) == 0
)

print(
    "Product relationship valid:",
    len(product_check) == 0
)

print(
    "Seller relationship valid:",
    len(seller_check) == 0
)
# =============================================================
# DUPLICATE CHECK
# =============================================================

print("\n========================== DUPLICATE CHECK ==========================")


# -------------------------------------------------------------
# 1. CUSTOMERS
# -------------------------------------------------------------

print("\nCustomers duplicate Customer_id:")

print(
    customers["Customer_id"].duplicated().sum()
)


# -------------------------------------------------------------
# 2. ORDERS
# -------------------------------------------------------------

print("\nOrders duplicate order_id:")

print(
    orders["order_id"].duplicated().sum()
)


# -------------------------------------------------------------
# 3. PRODUCTS
# -------------------------------------------------------------

print("\nProducts duplicate product_id:")

print(
    products["product_id"].duplicated().sum()
)


# -------------------------------------------------------------
# 4. SELLERS
# -------------------------------------------------------------

print("\nSellers duplicate seller_id:")

print(
    seller["seller_id"].duplicated().sum()
)


# =============================================================
# DUPLICATE CHECK SUMMARY
# =============================================================

print("\n========================== DUPLICATE CHECK SUMMARY ==========================")

print(
    "Duplicate Customer IDs:",
    customers["Customer_id"].duplicated().sum()
)

print(
    "Duplicate Order IDs:",
    orders["order_id"].duplicated().sum()
)

print(
    "Duplicate Product IDs:",
    products["product_id"].duplicated().sum()
)

print(
    "Duplicate Seller IDs:",
    seller["seller_id"].duplicated().sum()
)
# =============================================================
# FEATURE ENGINEERING
# =============================================================

print("\n========================== FEATURE ENGINEERING ==========================")


# -------------------------------------------------------------
# 1. CHECK EXISTING FEATURES
# -------------------------------------------------------------

print("\nExisting order features:")

print(
    orders[
        [
            "purchase_year",
            "purchase_month",
            "purchase_day",
            "purchase_day_name",
            "purchase_hour",
            "is_weekend",
            "delivery_days",
            "delivery_delay_days",
            "late_delivery"
        ]
    ].head()
)


# -------------------------------------------------------------
# 2. CREATE DELIVERY STATUS
# -------------------------------------------------------------

orders["delivery_status"] = np.where(
    orders["order_status"] == "delivered",
    "Delivered",
    "Not Delivered"
)


# -------------------------------------------------------------
# 3. CREATE ORDER VALUE
# -------------------------------------------------------------

order_value = (
    order_items
    .groupby("order_id")["price"]
    .sum()
    .reset_index()
)

order_value.rename(
    columns={"price": "order_value"},
    inplace=True
)


# -------------------------------------------------------------
# 4. MERGE ORDER VALUE INTO ORDERS
# -------------------------------------------------------------

orders = orders.merge(
    order_value,
    on="order_id",
    how="left"
)


# -------------------------------------------------------------
# 5. CREATE TOTAL FREIGHT VALUE
# -------------------------------------------------------------

freight_value = (
    order_items
    .groupby("order_id")["freight_value"]
    .sum()
    .reset_index()
)

freight_value.rename(
    columns={"freight_value": "total_freight_value"},
    inplace=True
)


# -------------------------------------------------------------
# 6. MERGE FREIGHT VALUE INTO ORDERS
# -------------------------------------------------------------

orders = orders.merge(
    freight_value,
    on="order_id",
    how="left"
)


# -------------------------------------------------------------
# 7. CREATE TOTAL ORDER COST
# -------------------------------------------------------------

orders["total_order_cost"] = (
    orders["order_value"] +
    orders["total_freight_value"]
)


# =============================================================
# CHECK NEW FEATURES
# =============================================================

print("\n========================== NEW FEATURES ==========================")

print(
    orders[
        [
            "order_id",
            "order_status",
            "delivery_status",
            "order_value",
            "total_freight_value",
            "total_order_cost"
        ]
    ].head(10)
)


# =============================================================
# FEATURE SUMMARY
# =============================================================

print("\n========================== FEATURE SUMMARY ==========================")

print(
    orders[
        [
            "order_value",
            "total_freight_value",
            "total_order_cost"
        ]
    ].describe()
)
# =============================================================
# EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================

print("\n========================== EDA ==========================")


# =============================================================
# 1. TOTAL ORDERS
# =============================================================

print("\n========================== ORDER OVERVIEW ==========================")

total_orders = orders["order_id"].nunique()

print(
    "Total Orders:",
    total_orders
)


# =============================================================
# 2. ORDER STATUS
# =============================================================

print("\n========================== ORDER STATUS ==========================")

order_status = (
    orders["order_status"]
    .value_counts()
)

print(order_status)


# =============================================================
# 3. DELIVERED ORDERS
# =============================================================

delivered_orders = orders[
    orders["order_status"] == "delivered"
]

print(
    "\nDelivered Orders:",
    len(delivered_orders)
)


# =============================================================
# 4. DELIVERY RATE
# =============================================================

delivery_rate = (
    len(delivered_orders)
    /
    total_orders
    *
    100
)

print(
    "Delivery Rate:",
    round(delivery_rate, 2),
    "%"
)


# =============================================================
# 5. TOTAL REVENUE
# =============================================================

total_revenue = orders[
    "order_value"
].sum()

print(
    "\nTotal Revenue:",
    round(total_revenue, 2)
)


# =============================================================
# 6. TOTAL FREIGHT
# =============================================================

total_freight = orders[
    "total_freight_value"
].sum()

print(
    "Total Freight:",
    round(total_freight, 2)
)


# =============================================================
# 7. TOTAL ORDER COST
# =============================================================

total_order_cost = orders[
    "total_order_cost"
].sum()

print(
    "Total Order Cost:",
    round(total_order_cost, 2)
)


# =============================================================
# 8. AVERAGE ORDER VALUE
# =============================================================

average_order_value = orders[
    "order_value"
].mean()

print(
    "Average Order Value:",
    round(average_order_value, 2)
)
# =============================================================
# MONTHLY SALES ANALYSIS
# =============================================================

print("\n========================== MONTHLY SALES ==========================")

monthly_sales = (
    orders
    .groupby("purchase_month")["order_value"]
    .sum()
    .reset_index()
)

monthly_sales.rename(
    columns={
        "order_value": "revenue"
    },
    inplace=True
)

print(monthly_sales)
# =============================================================
# TOP PRODUCTS
# =============================================================

print("\n========================== TOP PRODUCTS ==========================")

top_products = (
    order_items
    .groupby("product_id")
    .agg(
        total_sales=("price", "sum"),
        number_of_orders=("order_id", "nunique")
    )
    .sort_values(
        "total_sales",
        ascending=False
    )
    .head(10)
)

print(top_products)
# =============================================================
# TOP SELLERS
# =============================================================

print("\n========================== TOP SELLERS ==========================")

top_sellers = (
    order_items
    .groupby("seller_id")
    .agg(
        total_sales=("price", "sum"),
        number_of_orders=("order_id", "nunique")
    )
    .sort_values(
        "total_sales",
        ascending=False
    )
    .head(10)
)

print(top_sellers)
# =============================================================
# CUSTOMER ANALYSIS
# =============================================================

print("\n========================== CUSTOMER ANALYSIS ==========================")


# =============================================================
# 1. TOTAL UNIQUE CUSTOMERS
# =============================================================

total_customers = customers["Customer_id"].nunique()

print(
    "\nTotal Unique Customers:",
    total_customers
)


# =============================================================
# 2. TOTAL CUSTOMERS BY STATE
# =============================================================

customers_by_state = (
    customers
    .groupby("customer_state")["Customer_id"]
    .nunique()
    .sort_values(
        ascending=False
    )
)

print("\n========================== CUSTOMERS BY STATE ==========================")

print(
    customers_by_state.head(10)
)


# =============================================================
# 3. TOTAL CUSTOMERS BY CITY
# =============================================================

customers_by_city = (
    customers
    .groupby("customer_city")["Customer_id"]
    .nunique()
    .sort_values(
        ascending=False
    )
)

print("\n========================== TOP 10 CITIES BY CUSTOMERS ==========================")

print(
    customers_by_city.head(10)
)


# =============================================================
# 4. CUSTOMER STATE DISTRIBUTION
# =============================================================

customer_state_percentage = (
    customers["customer_state"]
    .value_counts(
        normalize=True
    )
    * 100
).round(2)

print("\n========================== CUSTOMER STATE PERCENTAGE ==========================")

print(
    customer_state_percentage.head(10)
)
# =============================================================
# STATE-WISE REVENUE ANALYSIS
# =============================================================

print("\n========================== STATE-WISE REVENUE ==========================")


# =============================================================
# 1. MERGE CUSTOMERS WITH ORDERS
# =============================================================

orders_customer = orders.merge(
    customers[
        [
            "Customer_id",
            "customer_state"
        ]
    ],
    left_on="customer_id",
    right_on="Customer_id",
    how="left"
)


# =============================================================
# 2. CALCULATE REVENUE BY STATE
# =============================================================

state_revenue = (
    orders_customer
    .groupby("customer_state")
    .agg(
        revenue=("order_value", "sum"),
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)


# =============================================================
# 3. DISPLAY TOP STATES
# =============================================================

print("\n========================== TOP STATES BY REVENUE ==========================")

print(
    state_revenue.head(10)
)


# =============================================================
# 4. AVERAGE ORDER VALUE BY STATE
# =============================================================

state_revenue["average_order_value"] = (
    state_revenue["revenue"]
    /
    state_revenue["orders"]
)


# =============================================================
# 5. DISPLAY COMPLETE STATE ANALYSIS
# =============================================================

print("\n========================== STATE PERFORMANCE ==========================")

print(
    state_revenue
    .head(10)
)


# =============================================================
# 6. TOP 5 REVENUE STATES
# =============================================================

print("\n========================== TOP 5 REVENUE STATES ==========================")

print(
    state_revenue
    .head(5)
)
# =============================================================
# PRODUCT CATEGORY ANALYSIS
# =============================================================

print("\n========================== PRODUCT CATEGORY ANALYSIS ==========================")


# =============================================================
# 1. MERGE ORDER ITEMS WITH PRODUCTS
# =============================================================

items_products = order_items.merge(
    products[
        [
            "product_id",
            "product_category_name"
        ]
    ],
    on="product_id",
    how="left"
)


# =============================================================
# 2. CHECK MISSING CATEGORIES AFTER MERGE
# =============================================================

print("\nMissing product categories:")

print(
    items_products["product_category_name"]
    .isna()
    .sum()
)


# =============================================================
# 3. CALCULATE CATEGORY REVENUE
# =============================================================

category_revenue = (
    items_products
    .groupby("product_category_name")
    .agg(
        revenue=("price", "sum"),
        number_of_items=("order_item_id", "count"),
        number_of_orders=("order_id", "nunique")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)


# =============================================================
# 4. DISPLAY TOP 10 CATEGORIES
# =============================================================

print("\n========================== TOP 10 CATEGORIES BY REVENUE ==========================")

print(
    category_revenue.head(10)
)


# =============================================================
# 5. CALCULATE AVERAGE ITEM PRICE
# =============================================================

category_revenue["average_item_price"] = (
    category_revenue["revenue"]
    /
    category_revenue["number_of_items"]
)


# =============================================================
# 6. DISPLAY CATEGORY PERFORMANCE
# =============================================================

print("\n========================== CATEGORY PERFORMANCE ==========================")

print(
    category_revenue.head(10)
)
# =============================================================
# PAYMENT ANALYSIS
# =============================================================

print("\n========================== PAYMENT ANALYSIS ==========================")


# =============================================================
# 1. PAYMENT TYPE DISTRIBUTION
# =============================================================

payment_type_count = (
    order_payments["payment_type"]
    .value_counts()
)

print("\n========================== PAYMENT TYPE COUNT ==========================")

print(payment_type_count)


# =============================================================
# 2. PAYMENT TYPE PERCENTAGE
# =============================================================

payment_type_percentage = (
    order_payments["payment_type"]
    .value_counts(normalize=True)
    * 100
).round(2)

print("\n========================== PAYMENT TYPE PERCENTAGE ==========================")

print(payment_type_percentage)


# =============================================================
# 3. TOTAL PAYMENT VALUE BY PAYMENT TYPE
# =============================================================

payment_value = (
    order_payments
    .groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\n========================== PAYMENT VALUE ==========================")

print(payment_value)


# =============================================================
# 4. AVERAGE PAYMENT VALUE
# =============================================================

average_payment = (
    order_payments
    .groupby("payment_type")["payment_value"]
    .mean()
    .sort_values(
        ascending=False
    )
)

print("\n========================== AVERAGE PAYMENT VALUE ==========================")

print(
    average_payment
)


# =============================================================
# 5. PAYMENT INSTALLMENTS
# =============================================================

average_installments = (
    order_payments
    .groupby("payment_type")["payment_installments"]
    .mean()
    .sort_values(
        ascending=False
    )
)

print("\n========================== AVERAGE INSTALLMENTS ==========================")

print(
    average_installments
)
# =============================================================
# REVIEW ANALYSIS
# =============================================================

print("\n========================== REVIEW ANALYSIS ==========================")


# =============================================================
# 1. REVIEW SCORE DISTRIBUTION
# =============================================================

print("\n========================== REVIEW SCORE DISTRIBUTION ==========================")

review_score_count = (
    order_reviews["review_score"]
    .value_counts()
    .sort_index()
)

print(
    review_score_count
)


# =============================================================
# 2. AVERAGE REVIEW SCORE
# =============================================================

average_review_score = (
    order_reviews["review_score"]
    .mean()
)

print("\nAverage Review Score:")

print(
    round(average_review_score, 2)
)


# =============================================================
# 3. REVIEW SCORE SUMMARY
# =============================================================

print("\n========================== REVIEW SCORE SUMMARY ==========================")

print(
    order_reviews["review_score"]
    .describe()
)
# =============================================================
# 4. POSITIVE AND NEGATIVE REVIEWS
# =============================================================

order_reviews["review_sentiment"] = np.where(
    order_reviews["review_score"] >= 4,
    "Positive",
    np.where(
        order_reviews["review_score"] <= 2,
        "Negative",
        "Neutral"
    )
)
print("\n========================== REVIEW SENTIMENT ==========================")
print(
    order_reviews["review_sentiment"]
    .value_counts()
)
# =============================================================
# 5. REVIEW SENTIMENT PERCENTAGE
# =============================================================

review_sentiment_percentage = (
    order_reviews["review_sentiment"]
    .value_counts(
        normalize=True
    )
    * 100
).round(2)


print("\n========================== REVIEW SENTIMENT PERCENTAGE ==========================")

print(
    review_sentiment_percentage
)


# =============================================================
# 6. REVIEWS WITH COMMENTS
# =============================================================

reviews_with_comments = order_reviews[
    order_reviews["review_comment_message"].notna()
]


print("\n========================== REVIEW COMMENTS ==========================")

print(
    "Reviews with comments:",
    len(reviews_with_comments)
)


print(
    "Reviews without comments:",
    len(order_reviews) - len(reviews_with_comments)
)


# =============================================================
# 7. REVIEW SCORE BY COMMENT STATUS
# =============================================================

comment_review_score = (
    order_reviews
    .groupby("has_comment")["review_score"]
    .mean()
)


print("\n========================== SCORE BY COMMENT STATUS ==========================")

print(
    comment_review_score
)
# =============================================================
# DELIVERY PERFORMANCE ANALYSIS
# =============================================================

print("\n========================== DELIVERY PERFORMANCE ==========================")


# =============================================================
# 1. DELIVERY TIME SUMMARY
# =============================================================

print("\n========================== DELIVERY TIME SUMMARY ==========================")

print(
    orders["delivery_days"]
    .describe()
)


# =============================================================
# 2. AVERAGE DELIVERY TIME
# =============================================================

average_delivery_days = (
    orders["delivery_days"]
    .mean()
)

print("\nAverage Delivery Time:")

print(
    round(average_delivery_days, 2),
    "days"
)


# =============================================================
# 3. MEDIAN DELIVERY TIME
# =============================================================

median_delivery_days = (
    orders["delivery_days"]
    .median()
)

print("\nMedian Delivery Time:")

print(
    round(median_delivery_days, 2),
    "days"
)


# =============================================================
# 4. ON-TIME VS LATE DELIVERY
# =============================================================

print("\n========================== DELIVERY STATUS ==========================")

print(
    orders["on_time_delivery"]
    .value_counts()
)


# =============================================================
# 5. ON-TIME DELIVERY PERCENTAGE
# =============================================================

on_time_percentage = (
    orders["on_time_delivery"]
    .value_counts(normalize=True)
    * 100
).round(2)

print("\n========================== DELIVERY STATUS PERCENTAGE ==========================")

print(
    on_time_percentage
)


# =============================================================
# 6. LATE DELIVERY PERCENTAGE
# =============================================================

late_delivery_percentage = (
    orders["late_delivery"]
    .mean()
    * 100
)

print("\nLate Delivery Percentage:")

print(
    round(late_delivery_percentage, 2),
    "%"
)


# =============================================================
# 7. DELIVERY DELAY SUMMARY
# =============================================================

print("\n========================== DELIVERY DELAY SUMMARY ==========================")

print(
    orders["delivery_delay_days"]
    .describe()
)


# =============================================================
# 8. ORDERS DELIVERED IN MORE THAN 30 DAYS
# =============================================================

print("\n========================== LONG DELIVERY CHECK ==========================")

print(
    "Orders delivered in more than 30 days:",
    (
        orders["delivery_days"] > 30
    ).sum()
)


print(
    "Orders delivered in more than 60 days:",
    (
        orders["delivery_days"] > 60
    ).sum()
)


print(
    "Orders delivered in more than 90 days:",
    (
        orders["delivery_days"] > 90
    ).sum()
)


# =============================================================
# 9. TOP 10 LONGEST DELIVERIES
# =============================================================

print("\n========================== TOP 10 LONGEST DELIVERIES ==========================")

longest_deliveries = (
    orders[
        [
            "order_id",
            "order_status",
            "delivery_days",
            "delivery_delay_days",
            "late_delivery"
        ]
    ]
    .dropna(
        subset=["delivery_days"]
    )
    .sort_values(
        "delivery_days",
        ascending=False
    )
    .head(10)
)

print(
    longest_deliveries
)


# =============================================================
# 10. DELIVERY PERFORMANCE BY ORDER STATUS
# =============================================================

print("\n========================== DELIVERY BY ORDER STATUS ==========================")

delivery_by_status = (
    orders
    .groupby("order_status")
    .agg(
        total_orders=("order_id", "nunique"),
        average_delivery_days=("delivery_days", "mean")
    )
    .sort_values(
        "total_orders",
        ascending=False
    )
)

print(
    delivery_by_status
)
# =============================================================
# DATA VISUALIZATION
# =============================================================

import matplotlib.pyplot as plt
import seaborn as sns

print("\n========================== DATA VISUALIZATION ==========================")


# =============================================================
# 1. ORDER STATUS DISTRIBUTION
# =============================================================

plt.figure(figsize=(10, 6))

orders["order_status"].value_counts().plot(
    kind="bar"
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =============================================================
# 2. MONTHLY ORDER TREND
# =============================================================

monthly_orders = (
    orders
    .groupby("purchase_month")
    ["order_id"]
    .nunique()
)

plt.figure(figsize=(10, 6))

monthly_orders.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Order Trend")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(range(1, 13))
plt.grid(True)
plt.tight_layout()
plt.show()


# =============================================================
# 3. TOP 10 PRODUCT CATEGORIES BY REVENUE
# =============================================================

top_categories = (
    category_revenue
    .head(10)
    .sort_values("revenue")
)

plt.figure(figsize=(10, 6))

top_categories["revenue"].plot(
    kind="barh"
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product Category")
plt.tight_layout()
plt.show()


# =============================================================
# 4. PAYMENT METHOD DISTRIBUTION
# =============================================================

plt.figure(figsize=(10, 6))

order_payments["payment_type"].value_counts().plot(
    kind="bar"
)

plt.title("Payment Method Distribution")
plt.xlabel("Payment Type")
plt.ylabel("Number of Payments")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =============================================================
# 5. REVIEW SCORE DISTRIBUTION
# =============================================================

plt.figure(figsize=(10, 6))

order_reviews["review_score"].value_counts().sort_index().plot(
    kind="bar"
)

plt.title("Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# =============================================================
# 6. DELIVERY DAYS DISTRIBUTION
# =============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    orders["delivery_days"].dropna(),
    bins=30,
    kde=True
)

plt.title("Delivery Time Distribution")
plt.xlabel("Delivery Days")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.show()


# =============================================================
# 7. TOP 10 STATES BY REVENUE
# =============================================================

top_states = (
    state_revenue
    .head(10)
    .sort_values("revenue")
)

plt.figure(figsize=(10, 6))

top_states["revenue"].plot(
    kind="barh"
)

plt.title("Top 10 States by Revenue")
plt.xlabel("Revenue")
plt.ylabel("State")
plt.tight_layout()
plt.show()


# =============================================================
# 8. DELIVERY STATUS
# =============================================================

delivery_status = pd.Series({
    "On Time": (
        orders["on_time_delivery"] == 1
    ).sum(),

    "Late": (
        orders["late_delivery"] == 1
    ).sum()
})


plt.figure(figsize=(8, 6))

delivery_status.plot(
    kind="bar"
)

plt.title("On-Time vs Late Delivery")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
# =============================================================
# BUSINESS INSIGHTS
# =============================================================

print("\n========================== BUSINESS INSIGHTS ==========================")


# =============================================================
# 1. TOTAL ORDERS
# =============================================================

total_orders = orders["order_id"].nunique()

print("\nTotal Orders:")
print(total_orders)


# =============================================================
# 2. TOTAL CUSTOMERS
# =============================================================

total_customers = customers["Customer_unique_id"].nunique()

print("\nTotal Customers:")
print(total_customers)


# =============================================================
# 3. TOTAL PRODUCTS
# =============================================================

total_products = products["product_id"].nunique()

print("\nTotal Products:")
print(total_products)


# =============================================================
# 4. TOTAL SELLERS
# =============================================================

total_sellers = seller["seller_id"].nunique()

print("\nTotal Sellers:")
print(total_sellers)


# =============================================================
# 5. TOTAL REVENUE
# =============================================================

total_revenue = (
    order_items["price"]
    .sum()
)

print("\nTotal Revenue:")
print(round(total_revenue, 2))


# =============================================================
# 6. AVERAGE ORDER VALUE
# =============================================================

order_revenue = (
    order_items
    .groupby("order_id")["price"]
    .sum()
)

average_order_value = (
    order_revenue.mean()
)

print("\nAverage Order Value:")
print(round(average_order_value, 2))


# =============================================================
# 7. MOST COMMON PAYMENT METHOD
# =============================================================

most_common_payment = (
    order_payments["payment_type"]
    .value_counts()
    .idxmax()
)

print("\nMost Common Payment Method:")
print(most_common_payment)


# =============================================================
# 8. AVERAGE CUSTOMER RATING
# =============================================================

average_rating = (
    order_reviews["review_score"]
    .mean()
)

print("\nAverage Customer Rating:")
print(round(average_rating, 2))


# =============================================================
# 9. AVERAGE DELIVERY TIME
# =============================================================

average_delivery = (
    orders["delivery_days"]
    .mean()
)

print("\nAverage Delivery Time:")
print(round(average_delivery, 2), "days")


# =============================================================
# 10. LATE DELIVERY PERCENTAGE
# =============================================================

late_percentage = (
    orders["late_delivery"]
    .mean()
    * 100
)

print("\nLate Delivery Percentage:")
print(round(late_percentage, 2), "%")


# =============================================================
# 11. TOP PRODUCT CATEGORY
# =============================================================

top_category = (
    category_revenue
    .sort_values(
        "revenue",
        ascending=False
    )
    .head(1)
)

print("\nTop Product Category:")

print(top_category)


# =============================================================
# 12. TOP STATE BY REVENUE
# =============================================================

top_state = (
    state_revenue
    .sort_values(
        "revenue",
        ascending=False
    )
    .head(1)
)

print("\nTop State by Revenue:")

print(top_state)

# =============================================================
#FINAL SUMMARY
# =============================================================

print("\n========================== FINAL SUMMARY ==========================")

print(
    "The Olist e-commerce dataset was analyzed to understand "
    "orders, customers, products, sellers, payments, reviews "
    "and delivery performance."
)

print(
    "Data cleaning and quality checks were performed before "
    "the exploratory analysis."
)

print(
    "The analysis identified important patterns in revenue, "
    "customer behavior, payment methods, product categories "
    "and delivery performance."
)
# =============================================================
# SAVE CLEANED DATA
# =============================================================

import os

os.makedirs("output", exist_ok=True)

customers.to_csv(
    "output/customers_cleaned.csv",
    index=False
)

orders.to_csv(
    "output/orders_cleaned.csv",
    index=False
)

products.to_csv(
    "output/products_cleaned.csv",
    index=False
)

seller.to_csv(
    "output/sellers_cleaned.csv",
    index=False
)

order_items.to_csv(
    "output/order_items_cleaned.csv",
    index=False
)

order_payments.to_csv(
    "output/payments_cleaned.csv",
    index=False
)

order_reviews.to_csv(
    "output/reviews_cleaned.csv",
    index=False
)

print("\nCleaned data saved successfully.")
# =============================================================
# SAVE BUSINESS RESULTS
# =============================================================

with pd.ExcelWriter(
    "output/olist_analysis_results.xlsx"
) as writer:

    orders["order_status"].value_counts().to_frame(
        "Order_Count"
    ).to_excel(
        writer,
        sheet_name="Order_Status"
    )

    order_payments["payment_type"].value_counts().to_frame(
        "Payment_Count"
    ).to_excel(
        writer,
        sheet_name="Payment_Method"
    )

    order_reviews["review_score"].value_counts().sort_index().to_frame(
        "Review_Count"
    ).to_excel(
        writer,
        sheet_name="Review_Score"
    )

    valid_delivery[
        [
            "order_id",
            "delivery_days",
            "delivery_delay_days",
            "late_delivery"
        ]
    ].to_excel(
        writer,
        sheet_name="Delivery_Analysis",
        index=False
    )

print("Analysis results saved successfully.")