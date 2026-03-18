WITH latest_prices AS (
    SELECT DISTINCT ON (material_id)
        material_id,
        price
    FROM prices
    WHERE material_id IS NOT NULL
    ORDER BY material_id, effective_date DESC
),
product_material_cost AS (
    SELECT 
        s.product_id,
        SUM(sc.material_quantity * lp.price) AS total_material_cost_per_unit
    FROM specifications s
    JOIN specification_compositions sc ON s.id = sc.specification_id
    JOIN latest_prices lp ON sc.material_id = lp.material_id
    GROUP BY s.product_id
)
SELECT 
    c.name AS "Заказчик",
    SUM(oc.quantity * oc.price) AS "Общая стоимость заказа"
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_compositions oc ON o.id = oc.order_id
WHERE o.id = '2'
GROUP BY c.name;