CREATE TABLE products (
    id int primary key,
    ean bigint,
    title text,
    category text,
    vender text,
    price double precision,
    rating double precision,
    created_at timestamp
);
\copy products FROM '/tmp/data/products.csv' DELIMITER ',' CSV HEADER;