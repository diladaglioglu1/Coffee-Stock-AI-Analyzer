# SWE314 Web Programming Project 1 - Coffee Stock AI Analyzer

## Overview
This repository contains the **Coffee Stock AI Analyzer** — an AI-powered full-stack dashboard developed to simulate inventory intelligence for a gourmet coffee shop. The application helps business owners monitor inventory, analyze historical sales, and receive smart stock recommendations through AI.

## Repository Structure
```
Coffee-Stock-AI-Analyzer/
│
├── backend/                 # FastAPI backend application
│   │                        # Contains the REST API, database models,
│   │                        # business logic and AI integration layer
│
├── frontend/                # React + Vite frontend application
│   │                        # Implements the interactive dashboard UI
│   │                        # used to visualize inventory and AI insights
│
├── responsibilities/        # Individual team contribution documents
│   │                        # Each team member explains their tasks
│   │                        # and technical contributions to the project
│
├── REPORT.md                # Detailed project report required by the course
│   │                        # Explains the business problem, architecture,
│   │                        # implementation decisions and results
│
└── README.md                # Main project documentation
```
## Core Components

### Backend — FastAPI REST API (backend/)
A robust data layer that manages inventory and integrates with Generative AI.

**Features**

**Inventory Management:**  CRUD operations for coffee shop products.

**Data Simulation:** Scripts to generate realistic sales and waste trends.

**AI Integration:**  Integration with Groq API (Llama 3.3) to generate inventory advice.

**ORM Layer:**  SQLite database using SQLModel.

**Swagger UI:** Interactive API documentation.

### Frontend — React Dashboard (frontend/)
A modern, responsive user interface built for real-time inventory monitoring.

**Concepts covered:**

**State Management:** Handling product lists and analysis results via useState.

**Tailwind CSS:** Professional SaaS-style UI design and responsive layouts.

**Asynchronous Actions:** Fetching data and triggering AI analysis with loading states.

**Data Visualization:** Displaying stock levels and AI-generated insights clearly.


## Tech Stack


| Layer| Technology| 
|--------|----------|
Frontend | React 18, Vite, Tailwind CSS |
Backend | Python, FastAPI, SQLModel |
Database | SQLite |
AI Engine |  Groq API (Llama 3.3) |

## Quick Start

### Backend
```bash
cd backend  
python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  
python init_db.py  
python seed_sales.py  
python seed_waste.py  
uvicorn main:app --reload  
```
The API will be available at http://localhost:8000. Visit http://localhost:8000/docs for the interactive UI.

### Frontend
Open a new terminal and run:
```bash
cd frontend  
npm install  
npm run dev  
```
The dashboard will be available at http://localhost:5173.

Note: The backend must be running for the dashboard to fetch product and sales data.

## Environment Variables

Create a .env file inside backend:
```bash
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/coffee_stock_ai
GROQ_API_KEY=your__api_key_here
```
## Business Logic & AI

The system addresses the "Overstock vs. Understock" dilemma common in small businesses. By sending recent sales velocity and current stock levels to the Gemini AI, the application provides specific recommendations such as:

"Demand for Oat Milk is rising; increase order by 20% for the weekend."

"Syrup stock is stagnant; avoid reordering to prevent waste." 

## Project Architecture
The system follows a standard full-stack architecture.
```bash
React Dashboard (Frontend)
│
│ HTTP Requests
▼
FastAPI REST API (Backend)
│
│ SQLModel ORM
▼
SQLite Database
│
▼
AI Service 
```

## Team Responsibilities

This project was developed by a five-member team.

| Role | Responsibility |
|-----|----------------|
Database Engineer | Designed relational schema and mock data generation |
AI Engineer | Implemented Gemini AI integration |
Backend Developer | Built FastAPI endpoints and business logic |
Frontend Developer | Implemented React dashboard |
Integration Engineer | Connected frontend and backend layers |

## Course Context
This project demonstrates:

- REST API design
- relational database modeling
- ORM with SQLModel
- frontend–backend integration
- generative AI integration

## Example Workflow

### Dashboard Overview
The system loads all products from the backend and displays real-time stock levels.

![Dashboard Overview](./screenshots/dashboard.png)
![Extended Dashboard](./screenshots/dashboard-more.png)
---

### Product Selection
User selects a product from the inventory list to analyze.

![Product Selection](./screenshots/product-selection.png)

---

### First AI Analysis (Cache Miss)
The system sends a request to the AI service.

- Source: GROQ AI
- Cache: Miss  
- Real-time analysis is generated

![AI Analysis - Miss](./screenshots/ai-miss.png)

---

### Second AI Analysis (Cache Hit)
The same request is triggered again.

- Source: Cache
- Cache: Hit  
- Response is returned instantly without calling AI

![AI Analysis - Hit](./screenshots/ai-hit.png)