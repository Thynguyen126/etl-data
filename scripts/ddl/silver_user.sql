CREATE TABLE users (
		id int primary key,
		email text,
		first_name text,
		last_name text,
		plan text,
		source text,
		seats integer,
		created_at timestamp,
		trail_ends_at timestamp,
		canceled_at timestamp,
		trial_converted boolean,
		active_subscription boolean,
		legacy_plan boolean,
		latitude float,
		longitude float,
		country varchar(2)
);
\copy users FROM '/tmp/data/users.csv' DELIMITER ',' CSV HEADER;
