# ============================================================
#  Topic 6: APIs with requests & REST
#  Covers: HTTP methods, REST concepts, requests library,
#          JSON parsing, error handling, real public APIs
#
#  Install: pip install requests
# ============================================================

import json

# ────────────────────────────────────────────────────────────
#  1. REST API CONCEPTS
# ────────────────────────────────────────────────────────────

print("=== 1. REST API Concepts ===")
print("""
  REST = Representational State Transfer

  HTTP Methods:
  ┌────────────┬────────────────────────────────┐
  │ GET        │ Read/fetch data                │
  │ POST       │ Create new data                │
  │ PUT        │ Update (replace entire record) │
  │ PATCH      │ Update (partial update)        │
  │ DELETE     │ Delete data                    │
  └────────────┴────────────────────────────────┘

  Status Codes:
  ┌───────┬────────────────────────────────────┐
  │ 200   │ OK — success                       │
  │ 201   │ Created — resource created         │
  │ 400   │ Bad Request — invalid input        │
  │ 401   │ Unauthorized — login required      │
  │ 403   │ Forbidden — no permission          │
  │ 404   │ Not Found                          │
  │ 500   │ Internal Server Error              │
  └───────┴────────────────────────────────────┘
""")


# ────────────────────────────────────────────────────────────
#  2. REQUESTS BASICS
# ────────────────────────────────────────────────────────────

print("=== 2. Using the requests Library ===")

try:
    import requests

    # ── GET request ───────────────────────────────────────
    print("\n  a) GET Request")
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

    print(f"  Status Code : {response.status_code}")
    print(f"  Content-Type: {response.headers.get('Content-Type')}")
    print(f"  URL         : {response.url}")

    data = response.json()
    print(f"  Title       : {data['title']}")
    print(f"  User ID     : {data['userId']}")
    print(f"  Body preview: {data['body'][:60]}...")

    # ── GET with params ───────────────────────────────────
    print("\n  b) GET with Query Parameters")
    params = {"userId": 1, "_limit": 3}
    response = requests.get("https://jsonplaceholder.typicode.com/posts", params=params)
    posts = response.json()
    print(f"  Fetched {len(posts)} posts for userId=1:")
    for post in posts:
        print(f"    [{post['id']}] {post['title'][:50]}")

    # ── POST request ──────────────────────────────────────
    print("\n  c) POST Request (Create)")
    new_post = {
        "title": "My New Post",
        "body": "This is the content of my post.",
        "userId": 1
    }
    response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json=new_post       # automatically sets Content-Type: application/json
    )
    created = response.json()
    print(f"  Status: {response.status_code}")   # 201 Created
    print(f"  Created post ID: {created['id']}")
    print(f"  Title: {created['title']}")

    # ── PUT request ───────────────────────────────────────
    print("\n  d) PUT Request (Update)")
    update_data = {
        "id": 1,
        "title": "Updated Title",
        "body": "Updated body content.",
        "userId": 1
    }
    response = requests.put(
        "https://jsonplaceholder.typicode.com/posts/1",
        json=update_data
    )
    print(f"  Status: {response.status_code}")
    print(f"  Updated: {response.json()['title']}")

    # ── PATCH request ─────────────────────────────────────
    print("\n  e) PATCH Request (Partial Update)")
    response = requests.patch(
        "https://jsonplaceholder.typicode.com/posts/1",
        json={"title": "Patched Title Only"}
    )
    print(f"  Status: {response.status_code}")
    print(f"  Patched title: {response.json()['title']}")

    # ── DELETE request ────────────────────────────────────
    print("\n  f) DELETE Request")
    response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
    print(f"  Status: {response.status_code}")   # 200 OK


    # ────────────────────────────────────────────────────────
    #  3. HEADERS & AUTHENTICATION
    # ────────────────────────────────────────────────────────

    print("\n=== 3. Headers & Authentication ===")

    # Custom headers
    headers = {
        "Authorization": "Bearer YOUR_TOKEN_HERE",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "MyApp/1.0",
    }
    # response = requests.get("https://api.example.com/data", headers=headers)

    # Basic Auth
    # response = requests.get("https://api.example.com", auth=("username", "password"))

    # API Key in params
    # response = requests.get("https://api.example.com", params={"api_key": "YOUR_KEY"})

    print("  Headers pattern shown (real token needed for secured APIs)")


    # ────────────────────────────────────────────────────────
    #  4. ERROR HANDLING
    # ────────────────────────────────────────────────────────

    print("\n=== 4. Error Handling ===")

    def safe_get(url, params=None, timeout=10):
        """Robust GET request with full error handling."""
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()    # raises HTTPError for 4xx/5xx
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Connection error: Cannot reach {url}")
        except requests.exceptions.Timeout:
            print(f"  ❌ Timeout: {url} took too long")
        except requests.exceptions.HTTPError as e:
            print(f"  ❌ HTTP error {e.response.status_code}: {e}")
        except requests.exceptions.JSONDecodeError:
            print(f"  ❌ Response is not valid JSON")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request failed: {e}")
        return None

    # Test with valid URL
    data = safe_get("https://jsonplaceholder.typicode.com/users/1")
    if data:
        print(f"  ✅ User: {data['name']} | Email: {data['email']}")

    # Test with 404
    data = safe_get("https://jsonplaceholder.typicode.com/posts/9999")
    # Test with bad URL
    data = safe_get("https://this-does-not-exist-xyz.com/api")


    # ────────────────────────────────────────────────────────
    #  5. SESSION — reuse connections
    # ────────────────────────────────────────────────────────

    print("\n=== 5. Session Object ===")

    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "MyPythonApp/1.0",
            "Accept": "application/json",
        })

        # All requests through this session share headers
        for user_id in [1, 2, 3]:
            res = session.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
            user = res.json()
            print(f"  [{user_id}] {user['name']:<20} {user['email']}")


    # ────────────────────────────────────────────────────────
    #  6. REAL PUBLIC APIs (no key needed)
    # ────────────────────────────────────────────────────────

    print("\n=== 6. Real Public APIs ===")

    # a) Open-Meteo Weather API
    print("\n  a) Weather API (Open-Meteo):")
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "current_weather": True,
    }
    data = safe_get(weather_url, params=params)
    if data:
        cw = data["current_weather"]
        print(f"     Delhi: {cw['temperature']}°C, wind {cw['windspeed']} km/h")

    # b) Dog CEO API
    print("\n  b) Dog CEO API (random dog image):")
    data = safe_get("https://dog.ceo/api/breeds/image/random")
    if data:
        print(f"     Image URL: {data['message'][:60]}...")

    # c) Numbers API
    print("\n  c) Numbers API:")
    data = safe_get("http://numbersapi.com/42/math?json")
    if data:
        print(f"     42 math fact: {data.get('text', 'N/A')}")

    # d) Rest Countries
    print("\n  d) Rest Countries API:")
    data = safe_get("https://restcountries.com/v3.1/name/india")
    if data and isinstance(data, list):
        country = data[0]
        print(f"     Country   : {country['name']['common']}")
        print(f"     Capital   : {country.get('capital', ['N/A'])[0]}")
        print(f"     Population: {country['population']:,}")
        print(f"     Region    : {country['region']}")


    # ────────────────────────────────────────────────────────
    #  7. SAVE API RESPONSE TO JSON FILE
    # ────────────────────────────────────────────────────────

    print("\n=== 7. Save API Response to File ===")

    response = requests.get("https://jsonplaceholder.typicode.com/users")
    users = response.json()

    with open("api_users.json", "w") as f:
        json.dump(users, f, indent=2)
    print(f"  ✅ Saved {len(users)} users to api_users.json")

    # Read back and display
    with open("api_users.json") as f:
        loaded = json.load(f)
    print("  Users loaded from file:")
    for u in loaded[:3]:
        print(f"    {u['id']}. {u['name']} ({u['username']})")

    import os; os.remove("api_users.json")

except ImportError:
    print("\n  ❌ 'requests' not installed.")
    print("  Run: pip install requests")
    print("\n  Here is what the code would do with requests installed:")
    print("  • GET/POST/PUT/PATCH/DELETE to REST APIs")
    print("  • Send JSON payloads, receive JSON responses")
    print("  • Handle errors: timeouts, 404s, auth failures")
    print("  • Use Sessions for persistent connections")
    print("  • Call real APIs: weather, countries, dog images")
