# Readly 📚

Readly is a Django-based online store for selling and delivering digital books (ebooks). It handles the full flow from browsing and cart management to checkout with Stripe or PayPal, and gives admins a sales-reporting dashboard out of the box.

## Features

- **Storefront** — homepage with featured products and a slider, category browsing, product detail pages, and live search
- **Cart & checkout** — session-based cart, checkout form, and order confirmation
- **Payments** — integrated **Stripe** (Payment Intents) and **PayPal** (IPN) checkout, with webhook handling for both
- **Digital delivery** — product cover images and PDF files stored and served via **Cloudinary**
- **Admin sales reports** — a custom Django admin dashboard (`reports` app) showing yearly, monthly, and weekly revenue statistics
- **Internationalization** — English and Arabic (`ar`) translations included
- **Production-ready settings** — configured for deployment on [Render](https://render.com) with Postgres (e.g. [Neon](https://neon.tech)), WhiteNoise for static files, and HTTPS/security hardening when `DEBUG=False`

## Tech Stack

- **Backend:** Django 5.2
- **Database:** PostgreSQL (via `dj-database-url` / `psycopg`)
- **Payments:** Stripe, PayPal (`django-paypal`)
- **Media storage:** Cloudinary (`django-cloudinary-storage`)
- **Static files:** WhiteNoise
- **Server:** Gunicorn
- **Deployment target:** Render

## Project Structure

```
django_store/    # Project settings, root URLs, WSGI/ASGI entrypoints
store/           # Storefront: products, categories, authors, cart, sliders
checkout/        # Checkout flow, Stripe/PayPal transactions & webhooks
reports/         # Admin-only sales reporting dashboard
static/          # CSS/JS assets
templates/       # Global templates (e.g. custom admin templates)
build.sh         # Render build script (install deps, collectstatic, migrate)
requirements.txt # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL database (or a `DATABASE_URL` connection string, e.g. from Neon)
- Stripe account (test keys are fine for local dev)
- PayPal Business account (sandbox works for local dev)
- Cloudinary account
- A Gmail account (or other SMTP provider) for sending emails

### 1. Clone the repository

```bash
git clone https://github.com/MohammadNoorM/Readly.git
cd Readly
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (either DATABASE_URL, or the individual DB_* vars below)
DATABASE_URL=postgresql://user:password@localhost:5432/readly

# Email
EMAIL_HOST_USER=you@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_ENDPOINT_SECRET=whsec_...

# PayPal
PAYPAL_TEST=True
PAYPAL_EMAIL=your-paypal-business-email@example.com

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 4. Run migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` for the storefront and `http://localhost:8000/admin` for the admin panel (including the sales reports dashboard).

## Deployment

This project is set up to deploy on **Render**:

- `build.sh` installs dependencies, runs `collectstatic`, and applies migrations on every deploy
- `RENDER_EXTERNAL_HOSTNAME` is automatically detected and added to `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS`
- Security settings (`SECURE_SSL_REDIRECT`, secure cookies, HSTS) are enabled automatically when `DEBUG=False`

Make sure to configure the same environment variables listed above in your Render service settings, along with a `DATABASE_URL` pointing at your production Postgres instance.

## License

This project is licensed under the MIT License.
