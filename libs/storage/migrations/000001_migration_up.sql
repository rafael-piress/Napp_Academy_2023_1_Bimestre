CREATE TABLE client (
  	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	client_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	phone_number VARCHAR(12),
);

CREATE TABLE sports_key_control (
  	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	sports_key_control_id SERIAL PRIMARY KEY,
	description VARCHAR(100) NOT NULL
);


CREATE TABLE sports_value_control (
  	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	sports_value_control_id SERIAL PRIMARY KEY,
	sports_key_control_id SERIAL,
	FOREIGN KEY (sports_key_control_id)
	REFERENCES sports_key_control(sports_key_control_id),
	description VARCHAR(100) NOT NULL
);


CREATE TABLE sports_key_value_occurrences (
  	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	occurrences_id SERIAL PRIMARY KEY,
	court_id SERIAL,
	weekday_id SERIAL,
	schedule_id SERIAL,
	client_id SERIAL,
	FOREIGN KEY (weekday_id) 
	REFERENCES sports_value_control(sports_value_control_id),
	FOREIGN KEY (schedule_id) 
	REFERENCES sports_value_control(sports_value_control_id),
	FOREIGN KEY (client_id) 
	REFERENCES client(client_id)
);

CREATE TABLE client_values (
  	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 	updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	client_id SERIAL,
	value DECIMAL,
	FOREIGN KEY (client_id) 
	REFERENCES client(client_id)
);

INSERT INTO sports_key_control(description) VALUES
	('Weekday'),
	('Schedule'),
	('Court');

INSERT INTO sports_value_control(sports_key_control_id, description) VALUES
	(1, 'Monday'),
	(1, 'Tuesday'),
	(1, 'Wednesday'),
	(1, 'Thursday'),
	(1, 'Friday'),
	(1, 'Saturday'),
	(1, 'Sunday');


INSERT INTO sports_value_control(sports_key_control_id, description) VALUES
	(2, '09hs - 10hs'),
	(2, '10hs - 11hs'),
	(2, '11hs - 12hs'),
	(2, '13hs - 14hs'),
	(2, '15hs - 16hs'),
	(2, '16hs - 17hs'),
	(2, '17hs - 18hs'),
	(2, '18hs - 19hs'),
	(2, '19hs - 20hs'),
	(2, '20hs - 21hs'),
	(2, '21hs - 22hs');


INSERT INTO sports_value_control(sports_key_control_id, description) VALUES
	(3, '1'),
	(3, '2'),
	(3, '3'),
	(3, '4');

INSERT INTO client(name, phone_number) VALUES 
('Your Name', '1960607070')

INSERT INTO sports_key_value_occurrences(court_id, weekday_id, schedule_id, client_id) VALUES 
(19, 1, 8, 1)

INSERT INTO sports_key_value_occurrences(court_id, weekday_id, schedule_id, client_id) VALUES 
(21, 2, 9, 1)
