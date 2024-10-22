# Event-Driven Microservices Application

## Overview

This project is a comprehensive event-driven microservices architecture designed to handle an online marketplace. It includes various services that work together seamlessly to manage products, orders, payments, inventory, notifications, and user authentication. The communication between services is handled using Kafka, ensuring that each service operates independently and scales efficiently. Additionally, SMTP email is integrated for sending notifications to users and administrators.

## Services

### 1. User Service
- **Purpose:** Manages user authentication and authorization.
- **Features:**
  - User registration and login with JWT-based authentication.
  - Role-based access control (RBAC) with two roles: User and Admin.
  - Admin can view and manage all users, while users can only view and update their own profiles.

### 2. Product Service
- **Purpose:** Manages product catalog.
- **Features:**
  - Admin can add, update, and delete products.
  - Users can view all products.
  - Each product contains details such as price, description, and stock status.

### 3. Order Service
- **Purpose:** Handles order creation and management.
- **Features:**
  - Users can place orders for products.
  - Orders are associated with users and stored with a status of "Unpaid" until payment is confirmed.
  - Orders communicate with the Inventory Service to ensure stock availability and update inventory levels after payment.

### 4. Payment Service
- **Purpose:** Manages payment processing using Stripe.
- **Features:**
  - Users can choose between "Cash on Delivery" or Stripe for online payments.
  - Payments are linked to orders, and successful payments trigger events that update order status and inventory levels.
  - Stripe payments redirect users to Stripe’s checkout and handle callback responses to confirm payment status.

### 5. Inventory Service
- **Purpose:** Manages product inventory.
- **Features:**
  - Updates stock levels when payments are confirmed.
  - Consumes Kafka events to handle inventory updates, ensuring consistency with orders and payments.

### 6. Notification Service
- **Purpose:** Sends notifications to users.
- **Features:**
  - Users receive notifications for various events, such as order creation and payment confirmation.
  - Admins can manage all notifications, while users can only view their own notifications.
  - **SMTP Email Integration:** Sends email notifications to users and admins for important events, such as successful order placements and payment confirmations.

## Technologies Used

- **FastAPI:** For building and running the microservices.
- **SQLModel:** ORM for database operations.
- **Kafka:** For event-driven communication between services.
- **Stripe:** For handling online payments.
- **Docker & Docker Compose:** Containerization of services for easy deployment.
- **PgAdmin:** For managing the PostgreSQL database.
- **OAuth2 & JWT:** For secure user authentication and authorization.
- **SMTP:** For sending email notifications.

## Architecture

The architecture follows a microservices approach where each service is independent and communicates asynchronously via Kafka. The use of Docker ensures that each service can be deployed and scaled independently. The user service provides authentication and role-based access control across all services.

### Key Flows

#### User Registration & Login
- Users register and log in via the User Service, receiving a JWT token for authentication.
- The JWT token is used to authenticate requests across other services.

#### Placing an Order
- Users place orders via the Order Service, which checks inventory and calculates the total price.
- Orders are initially marked as "Unpaid" and an event is produced for payment processing.

#### Processing Payment
- The Payment Service processes payments through Stripe.
- Upon successful payment, an event is produced to update the order status and inventory levels.

#### Inventory Management
- The Inventory Service updates stock levels based on events received from the Payment Service.
- Ensures that the stock is correctly managed and prevents overselling.

#### Notifications
- Users receive notifications for actions such as successful order placement and payment confirmation.
- Admins can view and manage all notifications, while users only see their own.
- **Email Notifications:** Critical updates and notifications are sent via email using SMTP.

## Environment Variables

For setting up the services, the following environment variables are used:

- `ADMIN_USERNAME`: The username for the initial admin user.
- `ADMIN_EMAIL`: The email for the initial admin user.
- `ADMIN_PASSWORD`: The password for the initial admin user.
- `DATABASE_URL`: The database connection URL.
- `KAFKA_BOOTSTRAP_SERVERS`: The Kafka bootstrap servers for event communication.
- `STRIPE_SECRET_KEY`: The Stripe secret key for processing payments.
- `SMTP_SERVER`: The SMTP server address for sending emails.
- `SMTP_PORT`: The port number for the SMTP server.
- `SMTP_USERNAME`: The username for the SMTP server authentication.
- `SMTP_PASSWORD`: The password for the SMTP server authentication.

## Getting Started

### Prerequisites

- Docker & Docker Compose
- PgAdmin for database management (optional)

### Running the Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ahadnaeem785/mart_project
   cd your-project

2. **Build and run the services:**
    - docker compose up --build

3. **Access the services**:
   (Use /docs after the url for Fast Api Swagger Ui)
   - User Service: http://localhost:8005
   - Product Service: http://localhost:8003
   - Order Service: http://localhost:8004
   - Payment Service: http://localhost:8001
   - Inventory Service: http://localhost:8002
   - Notification Service: http://localhost:8006
   - Kafka Ui port : http://localhost:8080

4. **Testing:**

   - Use tools like Postman or curl to interact with the APIs.
   - Ensure each service is running and accessible through the specified ports.
   - Test user registration, login, product management, order placement, and payment processing. 

5. **Conclusion:**
  - This project demonstrates the power and flexibility of microservices, combined with event-driven architecture. It showcases how independent services can work together to build a scalable, resilient, and maintainable system for an online marketplace.     
