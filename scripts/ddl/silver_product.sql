CREATE TABLE products (
    id int primary key,
    ean bigint,
    title text,
    category text,
    vender text,
    price double,
    rating smallint,
    created_at timestamp
);
\copy users FROM '/tmp/data/products.csv' DELIMITER ',' CSV HEADER;