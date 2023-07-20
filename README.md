Get All Products - http://127.0.0.1:5000/products Method = GET
Get Product By Id - http://127.0.0.1:5000/products/1 Method = GET
Add a Product - http://127.0.0.1:5000/products Method = POST
Sample Body Data For Postman { { "id": 5, "name": "Mac Book Pro", "price": 45.55, "description": "Amazing laptop with awesome security" } }

Get Cart Details - http://127.0.0.1:5000/cart?user_id=1234 Method = GET
Add Products To Cart - http://127.0.0.1:5000/cart/add Method = POST
Sample Body Data For Postman { "user_id": "user123", "product_id": 2, "quantity": 3 }

Delete Product From Cart - http://127.0.0.1:5000/cart/delete Method = POST
Sample Body Data For Postman { "user_id": "user123", "product_id": 2 }
