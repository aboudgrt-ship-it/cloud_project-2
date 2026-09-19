# Flask-JWT-Extended Functions Reference

### 1. `JWTManager(app)`
- **Role**: It is the main bridge between your Flask application and the JWT extension.
- **Usage**: It initializes the JWT system, allowing you to use decorators and token generation functions.

### 2. `create_access_token(identity=...)`
- **Role**: This function generates the actual encrypted string (the Token).
- **Parameter**: `identity` is usually the user's ID or username. This information is "encoded" inside the token.
- **Result**: Returns a long string that the client (mobile/browser) must store.

### 3. `@jwt_required()`
- **Role**: A "Decorator" placed above a route function.
- **Function**: It acts as a guard. If a request comes without a valid Token in the header, it automatically returns a `401 Unauthorized` error.

### 4. `get_jwt_identity()`
- **Role**: Used inside a protected route.
- **Function**: It extracts the `identity` (e.g., username) from the token sent by the user. This helps the server know exactly who is making the request.
