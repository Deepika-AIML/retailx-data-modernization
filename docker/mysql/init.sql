CREATE DATABASE IF NOT EXISTS retailx_source;
USE retailx_source;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    signup_date DATE
);

INSERT IGNORE INTO customers (customer_id, first_name, last_name, email, city, state, signup_date) VALUES
(101, 'Rahul', 'Sharma', 'rahul.sharma@gmail.com', 'Mumbai', 'Maharashtra', '2024-01-15'),
(102, 'Priya', 'Patel', 'priya.p@yahoo.com', 'Ahmedabad', 'Gujarat', '2024-02-01'),
(103, 'Amit', 'Kumar', 'amit.k@outlook.com', 'Delhi', 'Delhi', '2024-02-10'),
(104, 'Sneha', 'Reddy', 'sneha.r@gmail.com', 'Hyderabad', 'Telangana', '2024-03-05'),
(105, 'Vikram', 'Singh', 'vikram.s@gmail.com', 'Bangalore', 'Karnataka', '2024-03-20');