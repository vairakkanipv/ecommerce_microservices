import requests

BASE_PRODUCT = "http://localhost:8001/api"
BASE_ORDER   = "http://localhost:8002/api"

# ── Step 1: Login and get token ──────────────────────────────
print("\n--- Step 1: Getting JWT Token ---")
resp = requests.post(f"{BASE_PRODUCT}/token/", json={
    "username": "admin",
    "password": "admin123"
})
tokens = resp.json()
access_token = tokens["access"]
print(f"Access token received: {access_token[:40]}...")

headers = {"Authorization": f"Bearer {access_token}"}

# ── Step 2: Create a product ─────────────────────────────────
print("\n--- Step 2: Creating a Product ---")
resp = requests.post(f"{BASE_PRODUCT}/products/", json={
    "name":  "laptop hp i7",
    "price": 9799.99,
    "stock": 10
}, headers=headers)
product = resp.json()
product_id = product["id"]           # ← use the real id returned
print(f"Status: {resp.status_code}")
print(f"Response: {product}")

# ── Step 3: Check stock ──────────────────────────────────────
print("\n--- Step 3: Checking Stock ---")
resp = requests.get(f"{BASE_PRODUCT}/products/{product_id}/check_stock/", headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")

# ── Step 4: Place an order ───────────────────────────────────
print("\n--- Step 4: Placing an Order ---")
resp = requests.post(f"{BASE_ORDER}/orders/", json={
    "product_id": product_id,        # ← use the real id
    "quantity":   1
}, headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")

# ── Step 5: Check stock again (should be reduced by 2) ───────
print("\n--- Step 5: Checking Stock After Order (should be 8) ---")
resp = requests.get(f"{BASE_PRODUCT}/products/{product_id}/check_stock/", headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")

# ── Step 6: Test without token (should fail) ─────────────────
print("\n--- Step 6: Request Without Token (should be 401) ---")
resp = requests.get(f"{BASE_PRODUCT}/products/")
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")