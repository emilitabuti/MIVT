---
# MIVT Website

#### Video Demo: <https://youtu.be/6bTmQTbUXRc>

## Description
MIVT is a dynamic and user-friendly web application designed to simulate a virtual store for accessories. The platform provides functionalities for both merchants and customers, creating a comprehensive e-commerce experience. Merchants can easily register their products, including names, prices, and images, while customers can browse, add items to their cart, and complete purchases.

The project showcases a balance between simplicity for users and robust backend functionality, emphasizing practical coding skills learned through the CS50x course and beyond.

---

## Project Files and Their Purposes

### 1. **app.py**

app.py is the main application file for the project. It handles routing, user sessions, database interactions, and the core functionality of the web application. Below is an overview of its features and the key routes it defines.


### Key Routes

- /:
  Displays the product catalog and allows customers to add items to their cart or search for products.

- /carrinho:
  Shows the items in the customer's cart, calculates the total price, and allows them to proceed to checkout.

- /remover:
  Removes a specified product from the customer's cart.

- /compra:
  Allows customers to complete their purchase by providing address and payment details. Stores the purchase details in the database.

- /pedidos:
  Displays a list of past orders with detailed breakdowns for customers.

- /login and /registro:
  Manage customer login and registration with password hashing for secure authentication.

- /login_comerciante and /adicionar_produto:
  Merchants can log in and add products to the store.

- /logout and /logout_comerciante:
  Logout routes for customers and merchants, respectively.

---


### 2. **templates/**
This folder contains the HTML templates used to render the views of the web application. Each file corresponds to a specific route or functionality within the application, providing the user interface for customers and merchants.


### Templates Overview

- registro.html:
  Provides the registration form for new customers to create an account.

- login.html:
  Displays the login form for customers.

- login_comerciante.html:
  Offers the login interface for merchants.

- index.html:
  Serves as the main homepage displaying the catalog of products.

- carrinho.html:
  Customer's shopping cart, displaying selected items and total price.

-  compra.html:
  Presents the checkout form for completing purchases.

- pedidos.html:
  Lists all past orders placed by the customer.

- adicionar_produto.html:
  Allows merchants to add new products to the store's catalog.

-  info.html:
  Displays general information about the store.

---

### Notes
- The templates are rendered using Flask's Jinja2 templating engine.
- Dynamic content, such as product listings and user-specific data, is populated through variables passed from Flask routes.


### 3. **static/**
This folder holds static assets such as:
- style.css: The main stylesheet for the project, ensuring consistent and visually appealing UI design.
- uploads/: A directory for storing product images uploaded by merchants.

### 4. **README.md**
This file explains the structure, functionality, and key design decisions of the project. It serves as a guide for understanding how the application is built and operates.

### 5. **database.db**
The SQLite database that stores all the application's data, including:
- Product information (name, price, image path).
- Merchant and customer credentials (Usernames, hashed passwords, cart products, order details).

---

## Key Features

- **User Authentication**:
  - Secure login and logout functionality for both merchants and customers.
  - Passwords are securely hashed using werkzeug.security.

- **Merchant Functionality**:
  - Merchants can log in and manage their catalog by adding products with names, prices, and images.
  - Product images are dynamically uploaded and stored in the static/uploads directory.

- **Customer Functionality**:
  - Customers can browse a catalog of products, search by name, and add items to a shopping cart.
  - Customers can add, remove, and manage items in their cart, proceed to checkout, and place orders.

- **Order Management**:
  - Orders are stored with details like product quantities, subtotal, and delivery information.

- **Database Integration**:
  - Utilizes SQLite to store all application data, including products, user accounts, carts, and orders.

- **Responsive Design**:
  - Designed to adapt seamlessly to various screen sizes, ensuring accessibility across devices.


---

## Design Choices

### Database Structure
- A normalized database structure was chosen to maintain clarity and efficiency. For example:

  - Separate Tables: Products, users, and merchants are stored in dedicated tables to organize and isolate data.

  - Embedded Relationships: Relationships between users, products, and transactions are maintained by storing cart and order details as JSON fields within the users table.

### File Upload Handling
- Flask's request.files was used for handling image uploads. Uploaded images are stored in a dedicated directory, and their paths are referenced in the database.

### User Experience
- Simplicity and usability were key goals. The navigation and layout are intuitive, ensuring a smooth experience for both merchants and customers.

---

## Challenges and Considerations
- **Image Management**: Deciding where and how to store uploaded product images required balancing simplicity and scalability.
- **Scalability**: While SQLite is suitable for this prototype, a more robust database system may be needed for larger-scale implementations.

---

## Conclusion
MIVT is a testament to practical learning and showcases the application of foundational programming and web development skills. From managing user interactions to handling database operations, this project offers a well-rounded understanding of building a web application from scratch.

If you have any questions or feedback, feel free to reach out!