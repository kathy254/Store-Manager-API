# Store-Manager-API

[![Build Status](https://travis-ci.org/kathy254/Store-Manager-API.svg?branch=ft-store-attendant-161239141)](https://travis-ci.org/kathy254/Store-Manager-API)   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Store manager API

**Store Manager**
Store Manger API is a web application that makes it easier for store owners to manager their inventory, sales, and products to ensure they do not sale anything that is out of stock. This API is suitable for use by a single store.


**Motivation**
The purpose of Store Manager API is to make the lives of store owners and their attendants easier and more convenient. This application keeps track of all products and sales records.


**Code Style**
This API is constructed using python 3.6.6, flask, and flask RESTplus. Testing is done using pytest, and test coverage is done using pytest-cov

**Features**

The main features of this API include:
- The store attendant can see his personal sales records, though he will not be able to modify them
- The store attendant can add a product to a customer's cart
- The store attendant can search for all products using the product ID
- The store attendant can fetch a single product using its ID.
- The store owner can access the sales records of all store attendants.
- The store owner can add, delete and modify a product

**Endpoints**

Endpoint                                | Functionality
--------------------------------------- | -------------------------------------------------
GET /products | Fetch all products
GET /products/<productId> | Fetch a single product record
GET /sales | Fetch all sale records
GET /sales/<saleId> | Fetch a single sale record
POST /products | Create a product
POST /sales | Create a sale order
POST /users/register | Register a user
POST /users/login | Login a user

**Contributor**
Catherine Faith Omondi

**Acknowledgment**
- Head First Labs
- Prettyprinted.com
- Pre-bootcamp workshops
- Bootcamp
- Stackoverflow.com
