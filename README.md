# Smart Campus ERP & E-Commerce System - Database Setup

## Create Database

CREATE DATABASE studentdb;

USE studentdb;


# Users Table

CREATE TABLE users
(
    username VARCHAR(50),
    password VARCHAR(50)
);



INSERT INTO users
VALUES
(
    'admin',
    'admin123'
);


# Student Details Table


CREATE TABLE studentdetails
(
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    student_age INT,
    student_college VARCHAR(100),
    student_phone VARCHAR(15),
    student_branch VARCHAR(50),
    password VARCHAR(100)
);


# Products Table

CREATE TABLE products
(
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    quantity INT
);


Sample Products:


INSERT INTO products
(product_name, price, quantity)
VALUES
('Notebook',50,100),
('Pen',10,200),
('Calculator',500,25),
('Water Bottle',150,40),
('USB Drive',600,20);


---

# Orders Table


CREATE TABLE orders
(
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    product_name VARCHAR(100),
    quantity INT,
    total_amount DECIMAL(10,2)
);
```


# Cart Table


CREATE TABLE cart
(
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    product_name VARCHAR(100),
    quantity INT
);




# Useful Queries

## View Students


SELECT * FROM studentdetails;

## View Products


SELECT * FROM products;

## View Orders


SELECT * FROM orders;


## View Cart


SELECT * FROM cart;




# Search Student


SELECT *
FROM studentdetails
WHERE student_id = 1;




# Search Product


SELECT *
FROM products
WHERE product_id = 1;




# Update Student


UPDATE studentdetails
SET
student_name='Rahul',
student_phone='9876543210'
WHERE student_id=1;




# Update Product


UPDATE products
SET
price=250,
quantity=20
WHERE product_id=1;




# Delete Student


DELETE FROM studentdetails
WHERE student_id=1;




# Delete Product


DELETE FROM products
WHERE product_id=1;




# Reports Queries

## Total Students


SELECT COUNT(*)
FROM studentdetails;


## Total Products


SELECT COUNT(*)
FROM products;


## Total Orders


SELECT COUNT(*)
FROM orders;


## Total Revenue


SELECT SUM(total_amount)
FROM orders;

CREATE TABLE blog_posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(100),
    category VARCHAR(100),
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    parent_comment_id INT NULL,
    username VARCHAR(100),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES blog_posts(post_id)
);
