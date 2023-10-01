CREATE TABLE orders (
    order_code int primary key,
    distance float,
    final_deli_supplier text,
    destination_region text,
    destination_district text,
    departure_region text,
    seller_id int,
    route text,
    product_id int, 
    created_at datetime

);