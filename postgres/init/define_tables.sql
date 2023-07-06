\c dsx_group09

CREATE SCHEMA jal_op;

CREATE TABLE jal_op.departure (
    id UUID PRIMARY KEY NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    valid TIMESTAMP WITH TIME ZONE NOT NULL,
    flight_number VARCHAR(255) NOT NULL,
    departure_airport VARCHAR(255),
    destination_airport VARCHAR(255),
    flight_status VARCHAR(255),
    scheduled_departure_time TIMESTAMP WITH TIME ZONE,
    estimated_departure_time TIMESTAMP WITH TIME ZONE,
    actual_departure_time TIMESTAMP WITH TIME ZONE
);

CREATE TABLE jal_op.arrival (
    id UUID PRIMARY KEY NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    valid TIMESTAMP WITH TIME ZONE NOT NULL,
    flight_number VARCHAR(255) NOT NULL,
    origin_airport VARCHAR(255),
    arrival_airport VARCHAR(255),
    flight_status VARCHAR(255),
    scheduled_arrival_time TIMESTAMP WITH TIME ZONE,
    estimated_arrival_time TIMESTAMP WITH TIME ZONE,
    actual_arrival_time TIMESTAMP WITH TIME ZONE
);
