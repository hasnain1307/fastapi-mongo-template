class ErrorCodes:
    AUTHENTICATION_REQUIRED = "Authentication required."
    AUTHORIZATION_FAILED = "Authorization failed. User has no access."
    INVALID_TOKEN = "Invalid token."
    INVALID_CREDENTIALS = "Invalid credentials."
    EMAIL_TAKEN = "Email is already taken."
    REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."

    USERNAME_OR_EMAIL_ALREADY_EXISTS = "User with this username or email already exists"
    USER_NOT_FOUND = "User not found"

    TENANT_NOT_FOUND = "Tenant not found"
    TENANT_ALREADY_EXISTS = "Tenant with this name already exists"

    BOT_NOT_FOUND = "Bot not found"
    BOT_ALREADY_EXISTS = "Bot already exists"
