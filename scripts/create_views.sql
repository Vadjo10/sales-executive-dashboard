-- ============================================================================
-- VIEWS ANALÍTICAS PARA DASHBOARD POWER BI
-- Schema: warehouse
-- ============================================================================

-- 1. V_SALES_SUMMARY: Detalhamento de cada item de venda
-- Cada linha representa um produto dentro de um carrinho (sale line item)
CREATE OR REPLACE VIEW warehouse.v_sales_summary AS
WITH cart_items AS (
    SELECT
        c.id AS cart_id,
        c.userid AS user_id,
        c.date::date AS sale_date,
        (item ->> 'productId')::int AS product_id,
        (item ->> 'quantity')::int AS quantity
    FROM staging.stg_api_carts c
    CROSS JOIN LATERAL jsonb_array_elements(
        CASE
            WHEN c.products IS NOT NULL AND c.products != ''
            THEN c.products::jsonb
            ELSE '[]'::jsonb
        END
    ) AS item
)
SELECT
    ci.cart_id,
    ci.sale_date,
    ci.product_id,
    p.title AS product_name,
    p.category,
    p.price AS unit_price,
    ci.quantity,
    (p.price * ci.quantity) AS total_amount,
    COALESCE(u.id, 0) AS user_id,
    COALESCE(
        (u.name::jsonb ->> 'firstname') || ' ' || (u.name::jsonb ->> 'lastname'),
        'Unknown'
    ) AS user_name,
    COALESCE(u.address::jsonb ->> 'city', 'Unknown') AS city,
    COALESCE(u.address::jsonb -> 'geolocation' ->> 'lat', '0') AS lat,
    COALESCE(u.address::jsonb -> 'geolocation' ->> 'long', '0') AS lng,
    EXTRACT(YEAR FROM ci.sale_date)::int AS year,
    EXTRACT(MONTH FROM ci.sale_date)::int AS month,
    EXTRACT(QUARTER FROM ci.sale_date)::int AS quarter,
    TO_CHAR(ci.sale_date, 'YYYY-MM') AS year_month
FROM cart_items ci
LEFT JOIN staging.stg_api_products p ON ci.product_id = p.id
LEFT JOIN staging.stg_api_users u ON ci.user_id = u.id
WHERE ci.product_id IS NOT NULL;

COMMENT ON VIEW warehouse.v_sales_summary IS 'Detailed sales line items with product, user and date dimensions';


-- 2. V_MONTHLY_SALES: Métricas agregadas mensais
CREATE OR REPLACE VIEW warehouse.v_monthly_sales AS
SELECT
    year,
    month,
    year_month,
    COUNT(DISTINCT cart_id) AS total_transactions,
    COUNT(*) AS total_items_sold,
    SUM(quantity) AS total_quantity,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_ticket,
    COUNT(DISTINCT user_id) AS active_customers,
    COUNT(DISTINCT product_id) AS products_sold
FROM warehouse.v_sales_summary
GROUP BY year, month, year_month
ORDER BY year DESC, month DESC;

COMMENT ON VIEW warehouse.v_monthly_sales IS 'Monthly aggregated sales metrics for executive dashboard';


-- 3. V_CUSTOMER_ANALYSIS: Métricas por cliente
CREATE OR REPLACE VIEW warehouse.v_customer_analysis AS
SELECT
    user_id,
    user_name,
    city,
    COUNT(DISTINCT cart_id) AS total_orders,
    SUM(quantity) AS total_items_purchased,
    SUM(total_amount) AS total_spent,
    AVG(total_amount) AS avg_order_value,
    MIN(sale_date) AS first_purchase_date,
    MAX(sale_date) AS last_purchase_date,
    (MAX(sale_date) - MIN(sale_date)) AS customer_lifetime_days,
    COUNT(DISTINCT product_id) AS unique_products_bought
FROM warehouse.v_sales_summary
GROUP BY user_id, user_name, city
ORDER BY total_spent DESC;

COMMENT ON VIEW warehouse.v_customer_analysis IS 'Customer-level metrics for segmentation analysis';


-- 4. V_PRODUCT_PERFORMANCE: Performance por produto
CREATE OR REPLACE VIEW warehouse.v_product_performance AS
SELECT
    product_id,
    product_name,
    category,
    COUNT(DISTINCT cart_id) AS times_ordered,
    SUM(quantity) AS total_units_sold,
    SUM(total_amount) AS total_revenue,
    AVG(unit_price) AS avg_price,
    COUNT(DISTINCT user_id) AS unique_customers
FROM warehouse.v_sales_summary
GROUP BY product_id, product_name, category
ORDER BY total_revenue DESC;

COMMENT ON VIEW warehouse.v_product_performance IS 'Product-level performance metrics';


-- 5. V_DAILY_SALES: Vendas diárias para gráficos de tendência
CREATE OR REPLACE VIEW warehouse.v_daily_sales AS
SELECT
    sale_date,
    COUNT(DISTINCT cart_id) AS transactions,
    SUM(quantity) AS items_sold,
    SUM(total_amount) AS revenue,
    COUNT(DISTINCT user_id) AS active_users
FROM warehouse.v_sales_summary
GROUP BY sale_date
ORDER BY sale_date DESC;

COMMENT ON VIEW warehouse.v_daily_sales IS 'Daily sales metrics for trend charts';
