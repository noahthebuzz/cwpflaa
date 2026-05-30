# Frontend Setup & Development Guide

## Overview

The frontend is a **React 18** application built with **Vite** that provides an interactive user interface for solving puzzles, managing accounts, and viewing statistics. It communicates with the backend API via REST endpoints.

---

## Prerequisites

- **Node.js** 18+ and npm 9+
- **Backend running** on `http://localhost:8000` (for API calls)

Check your versions:

```bash
node --version
npm --version
```

---

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be running at `http://localhost:5173`

### 3. Test the Connection

The frontend automatically connects to the backend at `http://localhost:8000`. Test the setup by:

1. Open `http://localhost:5173` in your browser
2. You should see the app interface
3. Check browser console (F12) for any API errors

---

## Project Structure

```
frontend/
├── src/
│   ├── main.jsx              # Entry point
│   ├── App.jsx               # Root component
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Register.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Profile.jsx
│   │   ├── Puzzles/
│   │   │   ├── SudokuGame.jsx
│   │   │   ├── WordleGame.jsx
│   │   │   └── SchwedencrossGame.jsx
│   │   └── Common/
│   │       ├── Header.jsx
│   │       ├── Navigation.jsx
│   │       └── Footer.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Register.jsx
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Stats.jsx
│   │   └── Archive.jsx
│   ├── api/
│   │   ├── client.js         # Axios configuration
│   │   ├── auth.js           # Authentication endpoints
│   │   ├── puzzles.js        # Puzzle endpoints
│   │   └── stats.js          # Statistics endpoints
│   ├── hooks/
│   │   ├── useAuth.js        # Auth context hook
│   │   ├── usePuzzles.js     # Puzzle fetching hook
│   │   └── useToken.js       # Token management hook
│   ├── context/
│   │   └── AuthContext.jsx   # Authentication context
│   ├── styles/
│   │   ├── App.css
│   │   ├── variables.css
│   │   └── components.css
│   └── utils/
│       ├── storage.js        # LocalStorage helpers
│       └── validation.js     # Form validation
├── index.html
├── vite.config.js
├── package.json
└── .env                      # (Create locally, not in git)
```

---

## Configuration

### Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

If you change this, update `src/api/client.js`:

```javascript
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
```

---

## Available Scripts

### Development

```bash
npm run dev          # Start Vite dev server with hot reload
```

### Build

```bash
npm run build        # Build for production (output: dist/)
npm run preview      # Preview production build locally
```

### Linting & Formatting

```bash
npm run lint         # (Add ESLint if needed)
npm run format       # (Add Prettier if needed)
```

---

## API Integration

### Axios Client Setup

File: `src/api/client.js`

```javascript
import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

// Attach token to requests
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default client;
```

### Authentication API

File: `src/api/auth.js`

```javascript
import client from "./client";

export const generateUsername = async () => {
  const response = await client.post("/auth/generate-username");
  return response.data.username;
};

export const register = async (email, password, username) => {
  const response = await client.post("/auth/register", {
    email,
    password,
    username,
  });
  return response.data;
};

export const login = async (email, password) => {
  const response = await client.post("/auth/login", {
    email,
    password,
  });
  return response.data.access_token;
};

export const getCurrentUser = async () => {
  const response = await client.get("/auth/me");
  return response.data;
};
```

### Using in Components

```jsx
import { useEffect, useState } from "react";
import { login, getCurrentUser } from "../api/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const token = await login(email, password);
      localStorage.setItem("access_token", token);

      const user = await getCurrentUser();
      console.log("Logged in as:", user.username);
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div>
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        type="password"
      />
      <button onClick={handleLogin}>Login</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
```

---

## Authentication Context

Create a React Context to manage global auth state:

File: `src/context/AuthContext.jsx`

```jsx
import { createContext, useState, useEffect } from "react";
import { getCurrentUser } from "../api/auth";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const currentUser = await getCurrentUser();
          setUser(currentUser);
          setIsAuthenticated(true);
        } catch (err) {
          localStorage.removeItem("access_token");
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

---

## Component Examples

### Register Page

```jsx
import { useState } from "react";
import { register, generateUsername } from "../api/auth";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [suggestedUsername, setSuggestedUsername] = useState("");

  const handleSuggestUsername = async () => {
    const suggested = await generateUsername();
    setSuggestedUsername(suggested);
    setUsername(suggested);
  };

  const handleRegister = async () => {
    await register(email, password, username);
    // Redirect to login or auto-login
  };

  return (
    <div>
      <h1>Register</h1>
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        type="password"
      />
      <div>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <button onClick={handleSuggestUsername}>Suggest Username</button>
      </div>
      <button onClick={handleRegister}>Register</button>
    </div>
  );
}
```

---

## Styling

### Option 1: CSS Modules

```jsx
import styles from "./Button.module.css";

export default function Button({ children }) {
  return <button className={styles.button}>{children}</button>;
}
```

File: `Button.module.css`

```css
.button {
  background-color: #007bff;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}
```

### Option 2: Tailwind CSS

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Then use in components:

```jsx
<button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
  Click me
</button>
```

---

## Routing

Use React Router for navigation:

```bash
npm install react-router-dom
```

File: `src/App.jsx`

```jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}
```

---

## Development Workflow

### 1. Watch for Changes

Hot reload is automatic with Vite. Just save your files and the browser updates instantly.

### 2. Debug with Browser DevTools

- Press `F12` to open DevTools
- Check **Console** tab for errors
- Use **Network** tab to inspect API calls
- Check **Storage** → **Local Storage** for token

### 3. Use React DevTools

Install React DevTools extension for your browser to inspect component state and props.

---

## Troubleshooting

### 1. "CORS Error" or "Cannot POST /api/..."

**Problem**: Frontend can't communicate with backend

**Solution**:

1. Ensure backend is running on port 8000
2. Check `VITE_API_BASE_URL` in `.env`
3. Add CORS middleware to backend (if needed)

### 2. "Token not found" or "401 Unauthorized"

**Problem**: API requests are failing with 401

**Solution**:

1. Check localStorage has `access_token`
2. Try logging in again
3. Verify token is being sent in request header

### 3. Vite dev server not updating

**Problem**: Changes don't reflect in browser

**Solution**:

1. Check terminal for errors
2. Try `npm run dev` again
3. Clear browser cache (Ctrl+Shift+Delete)

---

## Production Build

### Build for Production

```bash
npm run build
```

Output goes to `dist/` folder. This is optimized for production.

### Deploy to VPS

1. Build the app:

   ```bash
   npm run build
   ```

2. Copy `dist/` folder to server:

   ```bash
   scp -r dist/ user@server:/var/www/cwpflaa/
   ```

3. Configure Nginx to serve the `dist/` folder (Phase 5)

---

## Next Steps

- **Phase 2**: Add puzzle fetching endpoints
- **Phase 3**: Build Sudoku, Wordle, and Schwedenrätsel game components
- **Phase 4**: Implement statistics dashboard
- **Phase 5**: Deploy to production

---

## Resources

- [React Docs](https://react.dev/)
- [Vite Docs](https://vitejs.dev/)
- [React Router Docs](https://reactrouter.com/)
- [Axios Docs](https://axios-http.com/)

---

## Questions?

Check [../COPILOT_CONTEXT.md](../COPILOT_CONTEXT.md) for detailed project architecture and planned features.
