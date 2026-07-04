# Microservices setup: auth_service + category_service + product_service

## Structure (same pattern as your auth_service)

```
category_service/
├── main.py
├── requirements.txt
├── database/
│   ├── connection.py      # own SQLite DB: category_service.db
│   └── dependencies.py    # get_db()
├── models/
│   └── category_model.py  # Category table
├── schema/
│   └── category_schema.py # Create / Update / Response schemas
├── router/
│   └── category_router.py # CRUD endpoints
├── exception/
│   └── category_exception.py
└── core/
    └── authentication.py  # verifies JWTs issued by auth_service

product_service/
├── main.py
├── requirements.txt
├── database/
│   ├── connection.py      # own SQLite DB: product_service.db
│   └── dependencies.py
├── models/
│   └── product_model.py   # Product table (stores category_id, no FK)
├── schema/
│   └── product_schema.py
├── router/
│   └── product_router.py  # CRUD endpoints
├── exception/
│   └── product_exception.py
└── core/
    ├── authentication.py       # same JWT verification as category_service
    └── category_client.py      # calls category_service over HTTP to check category_id
```

## Key microservice decisions

1. **Separate databases.** Each service gets its own SQLite file (swap for Postgres/MySQL in
   production, one DB per service). No cross-service foreign keys — `Product.category_id` is
   just a UUID column, validated at request time.

2. **Shared JWT, not shared code execution.** `category_service` and `product_service` don't call
   into `auth_service`'s Python code. They independently decode/verify the same JWT using an
   identical `SECRET_KEY` + `HS256`. This is the standard way to do auth in microservices — only
   `auth_service` issues tokens; every other service just verifies them.

   **You must set the same secret everywhere:**
   ```bash
   export JWT_SECRET_KEY="some-long-random-shared-secret"
   ```
   Set this in `auth_service`, `category_service`, and `product_service`. Your existing
   `core/gen_jwt.py` in `auth_service` should sign with this same env var.

3. **Cross-service validation via HTTP.** When you create/update a product, `product_service`
   calls `category_service`'s `GET /api/v1/category/{id}` to confirm the category is real, e.g.:
   ```bash
   export CATEGORY_SERVICE_URL="http://localhost:8001"
   ```

## Running everything locally

```bash
# terminal 1 — auth_service (your existing one)
export JWT_SECRET_KEY="some-long-random-shared-secret"
uvicorn main:app --reload --port 8000

# terminal 2 — category_service
export JWT_SECRET_KEY="some-long-random-shared-secret"
cd category_service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# terminal 3 — product_service
export JWT_SECRET_KEY="some-long-random-shared-secret"
export CATEGORY_SERVICE_URL="http://localhost:8001"
cd product_service
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

## Typical flow

1. `POST http://localhost:8000/api/v1/user/login` → get `access_token`
2. `POST http://localhost:8001/api/v1/category` with `Authorization: Bearer <token>`
   → create a category (admin role required), note its `id`
3. `POST http://localhost:8002/api/v1/product` with `Authorization: Bearer <token>` and that
   `category_id` → create a product. If the category_id doesn't exist, you get a `400` from
   product_service (it checked with category_service first).
4. `GET http://localhost:8002/api/v1/product?category_id=<id>` → list products in a category
   (public, no admin role required — same as your `/user/profile` vs admin split pattern).

## Notes / things to double check against your real auth_service

- I don't have your actual `core/authentication.py` / `core/gen_jwt.py` from `auth_service`, so
  I rebuilt an equivalent (`HTTPBearer` + `jose.jwt.decode`, `get_admin_user(roles_tuple)` as a
  dependency factory, `get_current_user`) to match how `admin_router.py` and `user_router.py`
  use them. **Make sure the algorithm, claim names (`role`, etc.), and secret line up exactly**
  with what your auth_service actually signs — otherwise verification will silently fail with
  401s everywhere.
- If you'd rather not duplicate `core/authentication.py` across 3 services, the cleaner
  long-term move is to pull it into a small shared pip-installable package (or a git submodule)
  all three services import — happy to set that up too if you want.
