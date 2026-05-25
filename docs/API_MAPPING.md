# API Endpoints Mapping

## Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /products | All products |
| GET | /products/:id | Single product |
| GET | /products/categories | All categories |
| GET | /products/category/:category | Products by category |

**Response fields:** id, title, price, description, category, image, rating

## Carts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /carts | All carts |
| GET | /carts/:id | Single cart |
| GET | /carts/user/:userId | Cart by user |

**Response fields:** id, userId, date, products[{productId, quantity}]

## Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users | All users |
| GET | /users/:id | Single user |

**Response fields:** id, email, username, password, name, address, phone

## Known Limitations

- No direct orders/sales endpoint
- Data is synthetic and static
- No authentication required
