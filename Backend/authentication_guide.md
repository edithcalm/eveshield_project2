# 🔐 User Authentication API

EveShield uses **Token-Based Authentication**. Users must authenticate via a token returned upon registration or login. Include this token in the `Authorization` header for all protected endpoints.

---

## 🛠️ Setting Up Authorization in Postman

1. In Postman, go to the **Authorization** tab.
2. Set the **Type** to `Bearer Token`.
3. Paste the token (received on registration/login) into the Token field.

Alternatively, go to the **Headers** tab and add:

```
Key:    Authorization
Value:  Token <your-auth-token>
```

---

## 🔁 Authentication Endpoints

### ✅ Register a New User

**Endpoint:**

```http
POST /api/users/auth/register/
```

**Description:**  
Creates a new user and returns a token for authentication.

**Request Body:**

```json
{
  "phone_number": "+254712345678",
  "username": "Test User",
  "password": "password123"
}
```

**Sample Response:**

```json
{
  "message": "New user registration successful!",

  "token": "generated-authentication-token"
}
```

---

### 🔑 Login an Existing User

**Endpoint:**

```http
POST /api/users/auth/login/
```

**Description:**  
Authenticates the user and returns a token.

**Request Body:**

```json
{
  "username": "example_user",
  "password": "securepassword"
}
```

**Sample Response:**

```json
{
  "tokens": {
    "access": "JWT_ACCESS_TOKEN",
    "refresh": "JWT_REFRESH_TOKEN"
  },
  "user": {
    "id": 1,
    "username": "Test User",
    "phone_number": "+254712345678"
  }
}
```

---

### 🔒 Logout a User

**Endpoint:**

```http
GET /api/users/auth/logout/
```

**Description:**  
Logs out the user and deletes the token.

**Request Headers:**

```http
Authorization: Token <generated-authentication-token>
```

**Sample Response:**

```json
{
  "message": "user logged out successfully!"
}
```

---

### 🔐 Accessing Protected Endpoints

Include the token in the `Authorization` header when calling any protected EveShield API:

```http
Authorization: Token <your-auth-token>
```
