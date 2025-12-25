# Python Three-Tier Architecture Example

This repository contains a modern implementation of a **Three-Tier Architecture** using Python, React, and Supabase.

![Task Dashboard Design](./task_dashboard_design)

## 🏗️ Architecture Overview

### 1. Presentation Tier (Frontend)
- **Located in**: `/frontend`
- **Tech Stack**: React 18, TypeScript, Vite, Framer Motion, Vanilla CSS.
- **Key Features**: 
  - Glassmorphism UI for a premium feel.
  - Responsive dashboard layout.
  - Real-time updates via API state management.
  - Dynamic animations and transitions.

### 2. Application Tier (Backend)
- **Located in**: `/backend`
- **Tech Stack**: FastAPI, Pydantic, Supabase Python Client.
- **Key Features**:
  - RESTful API endpoints for CRUD operations.
  - Middleware for CORS handling.
  - Decoupled logic from data storage.
  - Input validation and serialization.

### 3. Data Tier (Database)
- **Technology**: Supabase (PostgreSQL).
- **Setup**: 
  - Managed PostgreSQL instance.
  - Easily scalable and secure.
  - Communication is strictly via the Application Tier (Backend).

---

## 🚀 How to Run

### Prerequisites
- Python 3.9+
- Node.js & npm

### Step 1: Data Tier (Supabase)
1. Sign up at [Supabase.com](https://supabase.com/).
2. Create a new project.
3. Run the following SQL in the SQL Editor to create the `tasks` table:
   ```sql
   create table tasks (
     id uuid default gen_random_uuid() primary key,
     created_at timestamptz default now(),
     title text not null,
     status text default 'pending',
     priority text default 'medium'
   );
   ```
4. Copy your `Project URL` and `anon public key` from Settings > API.

### Step 2: Application Tier (Backend)
1. Navigate to `/backend`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update the `.env` file with your Supabase credentials:
   ```env
   SUPABASE_URL=your_url_here
   SUPABASE_KEY=your_key_here
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### Step 3: Presentation Tier (Frontend)
1. Navigate to `/frontend`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## 🔒 Security Note
In a true three-tier architecture, the **Presentation Tier** (browser) never talks to the **Data Tier** (database). All requests are funneled through the **Application Tier** (FastAPI), which enforces business rules and authorization before touching the data.
