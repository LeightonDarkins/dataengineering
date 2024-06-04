# Data Engineering Notes

## Course Details
Name: Data Engineering Essentials using SQL, Python and PySpark

## General Notes

### Relational Database Management Systems (RDBMSs)
- Oracle
- MySQL
- Postgres (used in this course)
- MS SQL Server
- Sybase
- IBM DB2

### Data Warehouse Technologies (Massively Parallel Processing (MPPs))
- Snowflake
- Databricks (used in this course)
- Teradata
- GCP BigQuery
- AWS RedShift
- Azure Synapse

### Purpose Built Databases
For specific use-cases use as specific technology:
- NoSQL or Document DBs (MongoDB, Cassandra)
- Search (Elastic Search, SolR)
- Graph DB (Neo4j)
- For Transactional Systems use RDBMSs
- For Data Feeds (non-transactional) used NoSQL
- For Search use-cases use NoSQL or Search (above)

### Data Warehouse & Data Lake (MPPs)

General flow looks like:

- Purpose Built DB ->
    - Data Lake/Warehouse ->
        - BI Reporting Tools
        - Machine Learning Applications
        - Direct Consumption by Consumers

A Data Warehouse includes Tables representing Data
A Data Lake is for File or Object Storage (typically S3 on AWS or GCS on GCP)

### Usage of RDBMSs or MPPs

- Buying a Product (transactional): RDBMS
- Tracking an Order (transactional): RDBMS
- Find out the profitability of my Organization: MPP
- Find out how revenue is trending this year: MPP
- Which Product Category is performing well?: MPP

### Differences between RDBMSs and MPPs

- Both contain Tables.

RDBMSs are primarily for transactional use-cases, also called Online Transaction Processing (OLTP).

MPPs are primarily used for Data Analysis or as a Decision Support System for a business. Also knows as Online Analytical Processing (OLAP).

Common ways for a user to interact with RDBMSs include:
- Mobile Apps
- Web Apps

Common ways for a user to interact with MPPs include:
- Reports
- Data Dashboards

RDBMSs tend to be a **source of truth** for data.

MPPs tend to be a Destination or Target for Data.

We pull data from RDBMSs and move it into MPPs for Analytical use-cases.

Across the board, SQL is used to query for data from either type of datastore (whether directly or indirectly (through BI tools etc.)).

## Setup and Installation
Installing Python, Postgres and PgAdmin

```
brew install python

brew install postgresql
createuser -s postgres
brew servies restart postgresql

brew install --cask pgadmin4
```
- Connection string is *localhost*
- User is *postgres*
- No Password

Exercise DB details:
- DB: retail_db
- USER: retail_user
- PASSWORD: retail_password

[Link for the Data repository](https://github.com/dgadiraju/data
)

## Data Model Overview

### Transactional and Non-Transactional Tables

- Orders and Order Items both change as Transactions occur (Transactional)
- Departments, Categories, Products and Customers do not change as Transactions occur (Non-Transactional)

### Problem Statement

*"Compute daily product revenue considering only Complete or Closed Orders"*

- "Daily" -  Order Date
- "Product" - Product ID
- "Revenue" - Order Item Subtotal
- "Complete or Closed" - Order Status

## SQL Syntax

### Order Of Execution

#### Steps in an SQL Query:

- FROM: Load Table data into memory.
- WHERE: Filter down to the data we want.
- GROUP BY (HAVING) / SELECT: Select and Group data (Grouping generally needs data to be Selected first).
- ORDER BY: Order the data for the user.

#### Example Query & Execution

```
SELECT order_date, count(*) AS order_count
FROM orders
WHERE order_status in (‘COMPLETE’, ‘CLOSED’)
GROUP BY order_date
ORDER BY order_count DESC
```

gets executed like this

- **FROM orders**: *load the data from the orders Table*
- **WHERE order_status in ('COMPLETE', 'CLOSED')**: *filter to just the Orders we want*
- **GROUP BY order_date, SELECT order_date, count(*) AS order_count**: *Select order_date and the count of Orders, then Group By the order_date.*
- **ORDER BY order_count DESC**: *Show the data in descending order by order_count.*

#### Query Restrictions

You cannot use Aggregations (sum(), count() etc.) to GROUP data.

You cannout use aliases in the WHERE clause (because the alias doesn't exist yet in the order of operations.)

### Identify and Count the DISTINCT Order Statuses

```
SELECT DISTINCT order_status
FROM orders;

SELECT count(DISTINCT order_status)
FROM orders;
```

### Get all Orders with order_status ClOSED or COMPLETE

```
SELECT * FROM orders
WHERE order_status in ('COMPLETE', 'CLOSED');
```

### Global Aggregations

- count()
- sum()
- min()
- max()
- avg()

#### Count all Orders with Status CLOSED or COMPLETE

```
SELECT count(*)
FROM orders
WHERE order_status in ('COMPLETE', 'CLOSED');
```

#### Get the total revenue from Order #2

```
SELECT SUM(order_item_subtotal)
FROM order_items
WHERE order_item_id = 2;
```

### GROUP_BY Aggregations (or By Key Aggregations)

#### Get the number of Orders in each Order Status

```
SELECT order_status, COUNT(*) AS order_count
FROM orders
GROUP BY 1
ORDER BY 2 DESC;
```
or, with named variables:
```
SELECT order_status, count(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;
```
#### Get the number of Orders for each Date

```
SELECT order_date, count(*) as order_count
FROM orders
GROUP BY order_date
ORDER BY order_count DESC;
```

#### Get the number of Orders for each Month

```
SELECT to_char(order_date, 'yyyy-MM') AS order_month, count(*) AS order_count
FROM orders
GROUP BY order_item_order_id
ORDER BY order_month DESC;
```

#### Get the total revenue for each Order ID

```
SELECT order_item_order_id, SUM(order_item_subtotal) AS order_revenue
FROM order_items
GROUP BY order_item_order_id
ORDER BY order_item_order_id DESC;
```

#### Round the total revenue to 2 decimal places

```
SELECT order_item_order_id, round(SUM(order_item_subtotal)::numeric, 2) AS order_revenue
FROM order_items
GROUP BY order_item_order_id
ORDER BY order_item_order_id DESC;
```

### Aggregate Results using GROUP BY and HAVING

#### Get only the rows where count(*) is 120 or over

```
SELECT order_date, count(*) as order_count
FROM orders
WHERE order_status IN ('COMPLETE', 'CLOSED')
GROUP BY order_date
    HAVING count(*) >= 120
ORDER BY order_count DESC;
```

### Inner Joins

An Inner Join only returns data that satisfies the *join condition*. An Order with no Order Items will not get returned in the following example:

#### Join two tables and select specific columns from each

```
SELECT o.order_date,
    oi.order_item_product_id,
    oi.order_item_subtotal
FROM orders AS o
    JOIN order_items AS oi
        ON o.order_id = oi.order_item_order_id
```

### Outer Joins

Outer Joins include all results whether they satisfy the *join condition* or not. In this case, the missing data will just be populated with null values.

```
SELECT o.order_id,
	o.order_date,
	oi.order_item_product_id,
	oi.order_item_subtotal
FROM orders AS o
	LEFT OUTER JOIN order_items AS oi
		ON o.order_id = oi.order_item_order_id
	ORDER BY o.order_id;
```

Outer Joins can be LEFT or RIGHT joins. From the example above, a LEFT OUTER JOIN will include all of data from Orders, and either matching data from Order Items or null values in their place. A RIGHT OUTER JOIN does the opposite. Including all of the data from Order Items and matching data (or null values) from Orders.

There is also the concept of a FULL OUTER JOIN, this just includes all data from all tables (or null values).

### Filtering and Aggregating JOIN Results
Filtering and aggregating results from JOINS looks similar to regular filters and aggregation, it's just important to remember to prefix the data with the correct Table alias from the JOIN condition.

```
SELECT o.order_date,
    oi.order_item_product_id,
    round(sum(oi.order_item_subtotal)::numeric, 2) AS order_revenue
FROM orders AS o
    JOIN order_items AS oi
        ON o.order_id = oi.order_item_order_id
WHERE o.order_status IN ('COMPLETE', 'CLOSED')
GROUP BY o.order_date, oi.order_item_product_id
ORDER BY o.order_date, order_revenue DESC;
```

### Database Views

For common actions like joining two tables you can create a View that contains the definition of that action. Once created, you can act on the View in the same way you'd act on a Table.

A View doesn't hold any data, just a definition for how to get a data set, whereas a Table contains raw data.

A View rexecutes the definition against the base Tables every time it's referenced.

To create a View, do this:

```
CREATE VIEW order_details_view
AS
SELECT o.*,
    oi.order_item_product_id,
    oi.order_item_subtotal
FROM orders AS o
    JOIN order_items AS oi
        ON o.order_id = oi.order_item_order_id;
```

You can then query this view like so:

```
SELECT * FROM order_details_view;
```

To update the view with new data/fields use:

```
CREATE OR REPLACE VIEW order_details_view...
```

But when adding new fields they must be added to the end of the field list.

### Common Table Expressions or Temporary Tables

CTEs are similar to Views, but not the same. Views are persisted in the Database where a CTE exists only in the scope of the current Query.

You can create and query a CTE like so:

```
WITH order_details_cte AS (
    SELECT o.*,
        oi.order_item_product_id,
        oi.order_item_subtotal,
        oi.order_item_id
    FROM orders AS o
        JOIN order_items AS oi
            ON o.order_id = oi.order_item_order_id
)

SELECT * FROM order_details_cte;
```

### Outer Join with Additional Conditions

Occasionally you may want to extend your join conditions to include specific requirements, like only including Products that were sold in a given month.

In this example we use an OUTER JOIN to get all of the Products Details and Order Details for Products that were sold in January 2014.

The WHERE clause isolates the cases where the Product Details are not present, indicating that those Products were NOT sold in January 2014.

```
SELECT *
FROM products AS p
    LEFT OUTER JOIN order_details AS od
        ON p.product_id = od.order_item_product_id
            AND to_char(od.order_date::timestamp, 'yyyy-MM') = '2014-01'
WHERE od.order_item_product_id IS NULL
```

### Create Table As (CTAS)

You can create tables from the data returned from a query:

```
CREATE TABLE order_count_by_status
AS
SELECT order_status, count(*) AS order_count
FROM orders
ORDER BY order_status
```

You can also create empty tables with the structure (columns and types) returned from a query by including and 'always false' WHERE clause:

```
CREATE TABLE order_table
AS
SELECT *
FROM orders
WHERE false; --or something like 1=2
```

### Cumulative Aggregations (OVER, PARTITION BY, ORDER BY)

A statement like **OVER (PARTITION BY xyz) AS output_column** creates a subset of items to run an aggregation (sum(), min(), max() etc.) over, then places that output into the query result table under a column you name (output_column in this case).

#### Get monthly revenue by SUMing order_revenue and PARTITIONing BY order_date

```
SELECT to_char(dr.order_date::timestamp, 'yyyy-MM') AS order_month
    dr.order_date,
    dr.order_revenue,
    sum(order_revenue) OVER (PARTITION BY to_char(dr.order_date::timestamp, 'yyyy-MM')) AS monthly_order_revenue
FROM daily_revenue AS dr
ORDER BY dr.order_date
```

#### Get total revenue by SUMing across the PARTITION of every result. Inserting a column called total_order_revenue into the output

```
SELECT dr.*
    sum(order_revenue) OVER (
        PARTITION BY 1
    ) AS total_order_revenue
FROM daily_revenue as dr
ORDER BY 1;
```

### Ranking

#### Ranking Functions

- **rank()**: Skips positions after equal Ranks have been found. If two people tied for the top score, they'd both get rank 1. The next highest scorer would get rank 3, because they're the 3rd in the list.
- **dense_rank()**: Does not skip positions. If two people tied for the top score, they'd both get rank 1. The next highest scorer would get rank 2, because their score is second highest.

#### Ranking Types

- Global Ranking: When you only use ORDER BY in the OVER statement. Ranks by all results.
    - ``rank() OVER(ORDER BY column_name_1 DESC``
- Key or Partition Key Ranking: When you use PARTITION BY in the OVER statement. Ranks by the given Partition.
    - ``rank() OVER(PARTITION BY column_name_1 ORDER BY column_name_2 DESC)``

#### Global Ranking example

```
SELECT dpr.*,
    rank() OVER (ORDER BY dpr.product_revenue DESC) as revenue_rank,
    dense_rank() OVER (ORDER BY dpr.product_revenue DESC) as revenue_rank_dense
FROM daily_product_revenue AS dpr
WHERE order_date = '2014-01-01 00:00:00.00'
```

#### Key or Partition Ranking Example

```
SELECT dpr.*,
    rank() OVER(
        PARTITION BY dpr.order_date ORDER BY dpr.order_revenue DESC
    ) as rnk,
    dense_rank() OVER(
        PARTITION BY dpr.order_date ORDER BY dpr.order_revenue DESC
    ) as drnk
FROM daily_product_revenue AS dpr
WHERE to_char(order_date::timestamp, 'yyyy-MM') = '2014-01';
```

### Filtering Data based on Global Ranks

Get the top 5 ranked Products by revenue from January 1st 2014

#### Using Sub-Queries

```
SELECT * FROM (
    SELECT dpr.*,
        rank() OVER (
            ORDER BY dpr.order_revenue DESC
        ) as rnk
    FROM daily_product_revenue AS dpr
    WHERE order_date = '2014-01-01 00:00:00.00'
) as q
WHERE rnk <= 5
```

#### Using CTEs

```
WITH daily_product_revenue_ranks AS (
	SELECT dpr.*,
		rank() OVER (ORDER BY dpr.order_revenue DESC) as rnk
	FROM daily_product_revenue AS dpr
	WHERE order_date = '2014-01-01 00:00:00.0’
)

SELECT * FROM daily_product_revenue_ranks
WHERE rnk <= 5
ORDER BY order_revenue DESC;

```

### Filtering Data based on Partition Ranks

Get the top 5 products by revenue per day in the month of January 2014

#### Using Sub-Queries

```
SELECT * FROM (
    SELECT dpr.*,
        rank() OVER (
            PARTITION BY dpr.order_date ORDER BY dpr.order_revenue DESC
        ) as rnk
    FROM daily_product_revenue AS dpr
    WHERE to_char(order_date::timestamp, 'yyyy-MM') = '2014-01'
) AS q
WHERE rnk <= 5
ORDER BY order_date, order_revenue
```

#### Using CTEs

```
WITH ranked_order_revenue AS (
	SELECT dpr.*,
		rank() OVER(
			PARTITION BY dpr.order_date ORDER BY dpr.order_revenue DESC
		) as rnk
	FROM daily_product_revenue AS dpr
	WHERE to_char(order_date::timestamp, 'yyyy-MM') = '2014-01'
)

SELECT * FROM ranked_order_revenue
	WHERE rnk <= 5
	ORDER BY order_date, order_revenue DESC;
```