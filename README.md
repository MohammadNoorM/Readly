# Django Store

An e-commerce web application built with Django 5.2. It supports product browsing, shopping cart management, and checkout via **Stripe** and **PayPal** payment gateways.

## Features

- **Product Catalog** — Browse products by category, search, and pagination
- **Featured Products & Sliders** — Highlight products and banners on the homepage
- **Shopping Cart** — Session-based cart with add/remove functionality
- **Checkout** — Supports Stripe and PayPal payment methods
- **Order Management** — Track orders and transactions via the admin panel
- **Admin Reports** — Custom reporting module in Django admin
- **Email Notifications** — SMTP email support (Gmail)
- **Internationalization** — i18n support with Arabic locale
- **Static Files** — Served with WhiteNoise

## Tech Stack

- Python 3.13
- Django 5.2
- SQLite
- Stripe API
- PayPal IPN (django-paypal)
- Pillow (image handling)
- WhiteNoise (static files)
- Gunicorn (production server)

## Project Structure

```
django_store/       # Project settings & configuration
store/              # Main store app (products, categories, cart, orders)
checkout/           # Checkout, payments & transactions
reports/            # Admin reports
templates/          # Global templates
static/             # Static assets (CSS, JS)
media/              # User-uploaded files
```

## Getting Started

### Prerequisites

- Python 3.13+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django_store
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root with the following:
   ```env
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   SITE_URL=http://localhost:8000
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_ENDPOINT_SECRET=your-stripe-webhook-secret
   PAYPAL_EMAIL=your-paypal-email
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   The app will be available at `http://localhost:8000`.

## Usage

- **Admin Panel** — `http://localhost:8000/admin/` to manage products, categories, orders, and reports.
- **Store** — `http://localhost:8000/` to browse the storefront.
- **Checkout** — `http://localhost:8000/checkout/` to complete a purchase.

## License

This project is for educational purposes.
