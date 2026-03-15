# SWE314 Web Programming Project 1 - Coffee Stock AI Analyzer

## Overview
This repository contains the **Coffee Stock AI Analyzer** — an AI-powered full-stack dashboard developed to simulate inventory intelligence for a gourmet coffee shop. The application helps business owners monitor inventory, analyze historical sales, and receive smart stock recommendations through Google Gemini AI.

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
                            # Provides project overview, setup instructions,
                            # architecture description and usage guide
```
## Core Components

### Backend — FastAPI REST API (backend/)
A robust data layer that manages inventory and integrates with Generative AI.

**Features**

**Inventory Management:**  CRUD operations for coffee shop products.

**Data Simulation:**  Specialized scripts to generate realistic sales and waste trends.

**AI Integration:** Integration with Google Gemini API to process inventory levels and sales velocity into natural language advice.

**ORM Layer:**  SQLite database management using SQLModel.

**Automated Documentation:** Interactive Swagger UI for API testing.

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
AI Engine | Google Gemini API |

## Quick Start

### 1. Start the Backend
Navigate to the backend folder and set up the environment:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python seed_sales.py
python seed_waste.py
uvicorn main:app --reload
```
The API will be available at http://localhost:8000. Visit http://localhost:8000/docs for the interactive UI.

### 2. Start a Frontend Version
Open a new terminal and run:
```bash
cd frontend
npm install
npm run dev
``` 
The dashboard will be available at http://localhost:5173.

Note: The backend must be running for the dashboard to fetch product and sales data.
⚠️ AI service is not configured. Please add GEMINI_API_KEY to your .env file.
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
Gemini AI Service
``` 

## API Endpoints
| Endpoint | Method | Description |
|--------|--------|-------------|
| /api/products | GET | Returns all products |
| /api/analyze/{id} | GET | Generates AI inventory recommendation |

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

This project was developed as part of the **Web Programming** course and demonstrates concepts such as:

- REST API design
- relational database modeling
- ORM with SQLModel
- frontend–backend integration
- generative AI integration
