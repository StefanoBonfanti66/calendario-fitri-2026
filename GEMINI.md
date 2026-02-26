# MTT Season Planner - Project Context & Rules

## 🚀 Overview
Project for managing the 2026 FITRI race calendar with multi-user support via Supabase.

## 🛠 Tech Stack
- **Frontend**: React 19 + TypeScript + Vite
- **Backend/Auth**: Supabase
- **Data Engine**: Python (Playwright for scraping)

## 🗄 Supabase Schema (PostgreSQL)

### Table: `public.user_plans`
- `id`: uuid (PK)
- `user_id`: uuid (FK auth.users)
- `race_id`: text (From races_full.json)
- `priority`: text (A, B, C)
- `cost`: numeric
- `note`: text
- **Security**: RLS enabled. Users can only CRUD their own rows.

### Table: `public.profiles`
- `id`: uuid (PK, FK auth.users)
- `full_name`: text
- **Security**: RLS enabled. Users can only Read/Update their own profile. Admin (`bonfantistefano4@gmail.com`) can read all.

## 🛡 Business Rules
- **Admin**: `bonfantistefano4@gmail.com` has access to the Admin Panel.
- **Recovery**: Password reset is handled via `supabase.auth.resetPasswordForEmail`.
- **Sync**: Always sync UI state with Supabase tables. Avoid `localStorage` for user-specific data.

## 🤖 AI Instructions
- When modifying the database, always provide the SQL script for the user to run in Supabase SQL Editor.
- Always check `app/src/supabaseClient.ts` for connection logic.
- Ensure `VITE_` prefix is used for environment variables in the Vite app.
