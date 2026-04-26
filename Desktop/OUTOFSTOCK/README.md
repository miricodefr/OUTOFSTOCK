# OUTOFSTOCK™ — Django E-Commerce Project
## ITC 4214 – Internet Programming (Level 6)

### Setup Instructions

1. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Mac/Linux
   venv\Scripts\activate           # Windows
   pip install -r requirements.txt
   ```

2. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server**
   ```bash
   python manage.py runserver
   ```

5. **Visit** `http://127.0.0.1:8000/`

---

### Project Structure

```
OUTOFSTOCK/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── outofstock_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── store/
    ├── models.py          # Profile, Category, Product, Review, CartItem, WishlistItem, Order, UsedCode
    ├── views.py           # All view logic
    ├── urls.py            # URL routing
    ├── admin.py           # Admin registrations
    ├── apps.py
    ├── migrations/        # 4 migration files
    ├── templates/store/   # HTML templates
    └── static/store/      # CSS and JS files
```

### Features Implemented
- **Dynamic catalogue** — browse products by category
- **Search & advanced filters** — search by name/brand, filter by category, price, brand, sort
- **Role-based security** — buyers, sellers, admins with different permissions
- **User registration & login/logout** — with form validation
- **Personalised dashboard** — cart, wishlist, orders, product management, admin panel
- **Product listings** — sellers/admins can create, edit, delete products with images
- **Shopping cart** — add/remove items, apply discount codes, checkout
- **Reviews & ratings** — logged-in users can rate and review products
- **Recommender** — suggests similar products from the same category
- **Discount codes** — `GIVEAPLS` (90% off), `10OFF` (10% off) — one-time use per account
- **Admin tools** — manage categories, users, products from the dashboard
