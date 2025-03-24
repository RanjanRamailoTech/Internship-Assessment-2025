from drf_yasg import openapi

CREATE_USER_API = {
    "operation_description": "Create a new user and send email verification link.",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="User's name"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="User's email", format="email"),
        },
        required=["email"],
    ),
    "responses": {
        201: openapi.Response(
            description="User created successfully",
            examples={
                "application/json": {
                    "data": {
                        "id": 1,
                        "name": "Jane",
                        "email": "jane@example.com"
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": [
                    {
                        "status_code": 400,
                        "type": "validation_error",
                        "params": ["email"],
                        "messages": ["Enter a valid email address."]
                    },
                    {
                        "status_code": 400,
                        "type": "validation_error",
                        "params": ["email"],
                        "messages": ["This field is required."]
                    },
                    {
                    "status_code": 400,
                        "type": "duplicate_error",
                        "params": ["email"],
                        "messages": ["Email already exists"]
                    },
                ]
            }
        ),
        500: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                    "status_code": 500,
                    "type": "service_unavailable",
                    "params": [],
                    "messages": ["Failed to connect to message broker"]
                }
            }
        )
    }
}

# Schema for LoginView
LOGIN_API = {
    "operation_description": "Log in a user and return JWT tokens.",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="User's email", format="email"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="User's password"),
        },
        required=["email", "password"],
    ),
    "responses": {
        200: openapi.Response(
            description="Login successful",
            examples={
                "application/json": {
                    "data": {
                        "refresh": "refresh-token",
                        "access": "access-token"
                    }
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "data": {
                        "message": "Invalid credentials"
                    }
                }
            }
        )
    }
}

# Schema for VerifyEmailView
VERIFY_EMAIL_API = {
    "operation_description": "Verify user email using the provided token.",
    "manual_parameters": [
        openapi.Parameter(
            "token",
            openapi.IN_PATH,
            description="Verification token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    "responses": {
        200: openapi.Response(
            description="Email verified",
            examples={
                "application/json": {
                    "data": {
                        "message": "Email verified successfully"
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Invalid token",
            examples={
                "application/json": {
                    "status_code": 400,
                    "type": "missing_field",
                    "params": ["token"],
                    "messages": ["Invalid or expired token"]
                }
            }
        )
    }
}