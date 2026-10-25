-- Production-style logical star schema (vendor-neutral teaching version)
CREATE TABLE dim_customer (
  customer_key BIGINT PRIMARY KEY,
  customer_id VARCHAR(64) UNIQUE,
  region VARCHAR(64),
  segment VARCHAR(64),
  valid_from TIMESTAMP,
  valid_to TIMESTAMP,
  is_current BOOLEAN
);

CREATE TABLE dim_product (
  product_key BIGINT PRIMARY KEY,
  product_id VARCHAR(64) UNIQUE,
  category VARCHAR(128),
  brand VARCHAR(128)
);

CREATE TABLE dim_date (
  date_key INTEGER PRIMARY KEY,
  calendar_date DATE,
  year INTEGER,
  month INTEGER,
  day INTEGER,
  week INTEGER
);

CREATE TABLE fact_order_line (
  order_id VARCHAR(64),
  customer_key BIGINT,
  product_key BIGINT,
  date_key INTEGER,
  quantity INTEGER,
  gross_revenue DECIMAL(18,2),
  discount DECIMAL(18,2),
  net_revenue DECIMAL(18,2),
  channel VARCHAR(64),
  PRIMARY KEY (order_id, product_key)
);
