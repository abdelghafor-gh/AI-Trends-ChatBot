# 🤖 AI Trends ChatBot

> 🌟 A modern AI-powered chat application for exploring and discussing AI trends with real-time insights and analytics.

[![Next.js](https://img.shields.io/badge/Next.js-13-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Auth-green?style=flat-square&logo=supabase)](https://supabase.com/)
[![DaisyUI](https://img.shields.io/badge/DaisyUI-4-ff69b4?style=flat-square)](https://daisyui.com/)

## 📚 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Frontend Architecture](#-frontend-architecture)
- [Data Pipeline](#-data-pipeline)
- [Backend Services](#-backend-services)
- [Getting Started](#-getting-started)
- [Environment Setup](#-environment-setup)
- [Contributing](#-contributing)

## 🎯 Overview

AI Trends ChatBot is a sophisticated web application that combines modern authentication, real-time chat capabilities, and AI-powered insights to provide users with an interactive platform for exploring artificial intelligence trends and developments.

## ✨ Features

### 🔐 Authentication & User Management
- Secure email-based authentication
- User profile customization
- Protected routes and middleware
- Email verification flow
- Session management

### 💬 Chat Interface
- Real-time messaging
- Modern, responsive design
- Mobile-friendly interface
- Dark/Light theme support
- Message history persistence

### 📊 Insights Dashboard
- AI trends visualization
- Real-time analytics
- Interactive data exploration
- Customizable views

## 🏗 Frontend Architecture

### 🛠 Tech Stack
- **Framework**: Next.js 13 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + DaisyUI
- **Authentication**: Supabase Auth
- **State Management**: React Hooks
- **Components**: Server & Client Components

### 📁 Project Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   └── confirm-email/
│   │   ├── dashboard/
│   │   │   ├── chat/
│   │   │   └── insights/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── UserNav.tsx
│   │   └── ChatInterface.tsx
│   ├── lib/
│   │   └── supabase/
│   └── styles/
└── public/
```

### 🎨 Key Components
- **UserNav**: User profile and navigation
- **ChatInterface**: Real-time chat functionality
- **DashboardLayout**: Protected layout with navigation
- **AuthForms**: Login and registration forms

## 🔄 Data Pipeline

> 🚧 **Coming Soon**: Azure Functions Implementation

### Planned Features
- Real-time data processing
- AI model integration
- Analytics pipeline
- Data transformation flows

## 🔧 Backend Services

> 🚧 **Coming Soon**: Backend Implementation

### Planned Features
- API endpoints
- Data persistence
- Business logic
- Integration services

## 🚀 Getting Started

### Frontend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-Trends-ChatBot.git
   cd AI-Trends-ChatBot
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   - Copy the `.env.example` file to `.env.local`
   ```bash
   cp .env.example .env.local
   ```
   - Fill in your environment variables in `.env.local`:
     ```env
     NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
     NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
     ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000) to see the application running.

### Build for Production

To create a production build:

```bash
npm run build
# or
yarn build
# or
pnpm build
```

Then start the production server:

```bash
npm start
# or
yarn start
# or
pnpm start
```

## ⚙️ Environment Setup

Required environment variables:
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_SITE_URL=your_site_url
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

---

<div align="center">

📝 **License** | MIT
:---: | :---:
🔨 **Status** | In Development
🌐 **Website** | [AI Trends ChatBot](#)
📧 **Contact** | [Your Email](#)

</div>
