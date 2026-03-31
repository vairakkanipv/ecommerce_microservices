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

# ── Step 2: Auth header used in all requests ─────────────────
headers = {"Authorization": f"Bearer {access_token}"}

# ── Step 3: Create a product ─────────────────────────────────
print("\n--- Step 2: Creating a Product ---")
resp = requests.post(f"{BASE_PRODUCT}/products/", json={
    "name":  "iPhone 15",
    "price": 999.99,
    "stock": 10
}, headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")

# ── Step 4: Check stock ──────────────────────────────────────
print("\n--- Step 3: Checking Stock ---")
resp = requests.get(f"{BASE_PRODUCT}/products/1/check_stock/", headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")

# ── Step 5: Place an order ───────────────────────────────────
print("\n--- Step 4: Placing an Order ---")
resp = requests.post(f"{BASE_ORDER}/orders/", json={
    "product_id": 1,
    "quantity":   2
}, headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")

# ── Step 6: Check stock again (should be reduced) ────────────
print("\n--- Step 5: Checking Stock After Order ---")
resp = requests.get(f"{BASE_PRODUCT}/products/1/check_stock/", headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")

# ── Step 7: Test without token (should fail) ─────────────────
print("\n--- Step 6: Request Without Token (should be 401) ---")
resp = requests.get(f"{BASE_PRODUCT}/products/")
print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")