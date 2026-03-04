# Basic Express Server with MongoDB Auth APIs

This project includes:
- Basic Express server setup
- MongoDB connection using Mongoose
- User schema with required fields:
  - Name
  - Email
  - Password
  - Age
  - Gender
  - Religion
  - Location
  - Profession
- Auth APIs:
  - `POST /api/auth/register`
  - `POST /api/auth/login`
- Postman collection for easy API testing

## How to run

### 1) Prerequisites
- Node.js 18+
- npm
- MongoDB running locally (or a MongoDB Atlas URI)

### 2) Install dependencies
```bash
npm install
```

### 3) Configure environment
Create your env file from the example:
```bash
cp .env.example .env
```

`.env` should look like:
```env
PORT=5000
MONGO_URI=mongodb://127.0.0.1:27017/azamkhan_db
```

If you use MongoDB Atlas, replace `MONGO_URI` with your Atlas connection string.

### 4) Start the API server
```bash
npm start
```

You should see logs similar to:
- `MongoDB connected successfully.`
- `Server running on port 5000`

### 5) Check server health
Open in browser or Postman:
- `GET http://localhost:5000/`

Expected response:
```json
{
  "message": "Express server is running."
}
```

## API Endpoints

### Register
`POST /api/auth/register`

Sample body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "Password@123",
  "age": 28,
  "gender": "Male",
  "religion": "Islam",
  "location": "Lahore",
  "profession": "Engineer"
}
```

### Login
`POST /api/auth/login`

Sample body:
```json
{
  "email": "john@example.com",
  "password": "Password@123"
}
```

## Test with Postman

### Option A: Use provided collection
1. Open Postman.
2. Import `postman/Auth-APIs.postman_collection.json`.
3. Ensure collection variable `baseUrl` is set to:
   - `http://localhost:5000`
4. Run requests in order:
   - `Register`
   - `Login`

### Option B: Create requests manually
- **Register**
  - Method: `POST`
  - URL: `http://localhost:5000/api/auth/register`
  - Body type: `raw` + `JSON`
  - Paste register sample payload

- **Login**
  - Method: `POST`
  - URL: `http://localhost:5000/api/auth/login`
  - Body type: `raw` + `JSON`
  - Paste login sample payload

## Run in VS Code

1. Open VS Code.
2. Go to **File > Open Folder...** and select this project folder (`AzamKhan`).
3. Open Terminal in VS Code (**Terminal > New Terminal**).
4. Run dependencies install:
   ```bash
   npm install
   ```
5. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```
6. (Optional) Start MongoDB locally if not already running.
7. Start server in VS Code terminal:
   ```bash
   npm start
   ```
8. Verify API is running by visiting:
   - `http://localhost:5000/`

### Debug mode in VS Code (optional)
1. Open **Run and Debug** panel (`Ctrl+Shift+D`).
2. Click **create a launch.json file** (if prompted).
3. Choose **Node.js**.
4. Use this basic config:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Run API",
      "program": "${workspaceFolder}/src/server.js"
    }
  ]
}
```

Then press **F5** to run under debugger.

