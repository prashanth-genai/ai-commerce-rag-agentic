"""
auth.py
--------
Authentication & Authorization module for the AI Gateway.

Supports:
✔ JWT Authentication
✔ API Key Validation
✔ Role-Based Access Control (RBAC)
✔ Token Expiry Enforcement
✔ Secure Error Responses

Used by: AI Gateway, Agent Services, RAG APIs
"""

import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from typing import Optional, Dict

# -----------------------------
# Secret Keys & Configurations
# -----------------------------
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
JWT_ALGORITHM = "HS256"
API_KEYS = {
    "internal-ai-service": "AI_INTERNAL_KEY_12345",
    "csr-portal": "CSR_KEY_67890",
    "mobile-app": "MOBILE_KEY_24680"
}

# Roles allowed per client type
ROLE_MAP = {
    "internal-ai-service": ["AI_AGENT"],
    "csr-portal": ["CSR", "ADMIN"],
    "mobile-app": ["CUSTOMER"]
}

# -----------------------------
# JWT Utility Functions
# -----------------------------

def generate_jwt(user_id: str, role: str, expires_in_minutes: int = 60) -> str:
    """
    Generate a signed JWT token for the API Gateway.
    """
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt(token: str) -> Dict:
    """
    Decode and validate JWT token.
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -----------------------------
# API Key Validation
# -----------------------------
def validate_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Validate API key for internal service-to-service communication.
    """
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API key")

    for client_name, key in API_KEYS.items():
        if x_api_key == key:
            return client_name

    raise HTTPException(status_code=401, detail="Invalid API key")

# -----------------------------
# Authorization (RBAC)
# -----------------------------
def authorize_role(client_name: str, required_role: str):
    """
    Ensure the calling client has the required role.
    """
    allowed_roles = ROLE_MAP.get(client_name, [])

    if required_role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied. Role '{required_role}' required."
        )

# -----------------------------
# Combined Authentication Wrapper
# -----------------------------
def authenticate_request(
    x_api_key: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
) -> Dict:
    """
    Main entrypoint for API Gateway authentication.
    Supports:
    - API Key auth (service-to-service)
    - JWT auth (end-user)
    """

    # 1. API Key Validation (internal services)
    if x_api_key:
        client_name = validate_api_key(x_api_key)
        return {"auth_type": "api_key", "client_name": client_name}

    # 2. JWT Validation (end-users / CSR / Admin)
    if authorization:
        token = authorization.replace("Bearer ", "")
        decoded = decode_jwt(token)
        return {"auth_type": "jwt", "payload": decoded}

    # If neither key nor JWT is provided
    raise HTTPException(status_code=401, detail="Unauthorized request")


# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    # Example JWT creation
    token = generate_jwt(user_id="U1001", role="CUSTOMER")
    print("Generated JWT:", token)

    # Decode JWT
    print("Decoded:", decode_jwt(token))

