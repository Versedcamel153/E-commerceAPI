
# API Documentation for E-commerce Product API

---

## 1. User API

### 1.1 List/Create Users

- **Endpoint:** `/users/`
- **Method:** `GET`, `POST`
- **Description:** List all users or create a new user.

**Request Body (POST):**
```json
{
  "email": "user@example.com",
  "username": "exampleUser",
  "password": "yourpassword"
}
```

**Responses:**
- **200 OK** (GET)
    - Returns a list of users.
- **201 Created** (POST)
    - Returns the created user object.

---

### 1.2 Retrieve/Update/Delete User

- **Endpoint:** `/users/<int:pk>/`
- **Method:** `GET`, `PUT`, `DELETE`
- **Description:** Retrieve, update, or delete a specific user by ID.

**Request Body (PUT):**
```json
{
  "email": "newemail@example.com",
  "username": "newUser",
  "password": "newpassword"
}
```

**Responses:**
- **200 OK** (GET)
    - Returns the user object.
- **204 No Content** (DELETE)
    - Successfully deleted the user.

---

## 2. Product API

### 2.1 Create Products

- **Endpoint:** `/products/create/`
- **Method:** `GET`, `POST`
- **Description:** List all products or create a new product.

**Request Body (POST):**
```json
{
  "name": "Product Name",
  "description": "Product Description",
  "price": 19.99,
  "category": 1,
  "stock_quantity": 10
}
```

**Responses:**
- **200 OK** (GET)
    - Returns a list of products.
- **201 Created** (POST)
    - Returns the created product object.

---

### 2.2 Retrieve/Update/Delete Product

- **Endpoint:** `/products/<int:pk>/`
- **Method:** `GET`, `PUT`, `DELETE`
- **Description:** Retrieve, update, or delete a specific product by ID.

**Request Body (PUT):**
```json
{
  "name": "Updated Product Name",
  "description": "Updated Description",
  "price": 25.00,
  "category": 1,
  "stock_quantity": 5
}
```

**Responses:**
- **200 OK** (GET)
    - Returns the product object.
- **204 No Content** (DELETE)
    - Successfully deleted the product.

---

## 3. Review API

### 3.1 List/Create Reviews for a Product

- **Endpoint:** `/products/<int:pk>/reviews/`
- **Method:** `GET`, `POST`
- **Description:** List all reviews for a specific product or create a new review.

**Request Body (POST):**
```json
{
  "rating": 5,
  "comment": "Excellent product!"
}
```

**Responses:**
- **200 OK** (GET)
    - Returns a list of reviews for the product.
- **201 Created** (POST)
    - Returns the created review object.

---

### 3.2 Retrieve/Update/Delete Review

- **Endpoint:** `/products/<int:pk>/reviews/<int:review_pk>/`
- **Method:** `GET`, `PUT`, `DELETE`
- **Description:** Retrieve, update, or delete a specific review by ID.

**Request Body (PUT):**
```json
{
  "rating": 4,
  "comment": "Very good product!"
}
```

**Responses:**
- **200 OK** (GET)
    - Returns the review object.
- **204 No Content** (DELETE)
    - Successfully deleted the review.

---

## 4. Cart API

### 4.1 Retrieve User's Cart

- **Endpoint:** `/cart/`
- **Method:** `GET`
- **Description:** Retrieve the authenticated user's shopping cart.

**Responses:**
- **200 OK**
    - Returns the cart details for the user.

---

### 4.2 Add Item to Cart

- **Endpoint:** `/cart/add/`
- **Method:** `POST`
- **Description:** Add an item to the user's cart.

**Request Body (POST):**
```json
{
  "product": 1,
  "quantity": 2
}
```

**Responses:**
- **201 Created**
    - Returns the cart item added.

---

### 4.3 Remove Item from Cart

- **Endpoint:** `/cart/<int:pk>/remove/`
- **Method:** `DELETE`
- **Description:** Remove an item from the user's cart.

**Responses:**
- **204 No Content**
    - Successfully removed the item from the cart.

---

## 5. Order API

### 5.1 Create Order

- **Endpoint:** `/orders/create/`
- **Method:** `POST`
- **Description:** Create a new order from the user's cart.

**Request Body (POST):**
```json
{
  "cart": 1
}
```

**Responses:**
- **201 Created**
    - Returns the created order object.

---

### 5.2 Retrieve Order Details

- **Endpoint:** `/orders/<int:pk>/`
- **Method:** `GET`
- **Description:** Retrieve the details of a specific order by ID.

**Responses:**
- **200 OK**
    - Returns the order object.
