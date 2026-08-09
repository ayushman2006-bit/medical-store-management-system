CREATE DATABASE IF NOT EXISTS pharmacy_db;

USE pharmacy_db;

CREATE TABLE IF NOT EXISTS medicines (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) DEFAULT NULL,
    quantity INT DEFAULT NULL,
    price DECIMAL(10,2) DEFAULT NULL,
    expiry DATE DEFAULT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS bills (
    bill_id INT NOT NULL AUTO_INCREMENT,
    bill_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (bill_id)
);

CREATE TABLE IF NOT EXISTS bill_items (
    item_id INT NOT NULL AUTO_INCREMENT,
    bill_id INT DEFAULT NULL,
    medicine_name VARCHAR(100) DEFAULT NULL,
    quantity INT DEFAULT NULL,
    price DECIMAL(10,2) DEFAULT NULL,
    subtotal DECIMAL(10,2) DEFAULT NULL,
    PRIMARY KEY (item_id),
    KEY bill_id (bill_id),
    CONSTRAINT bill_items_ibfk_1
        FOREIGN KEY (bill_id)
        REFERENCES bills (bill_id)
);