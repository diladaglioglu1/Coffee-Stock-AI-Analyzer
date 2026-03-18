# SWE314 Web Programming Project 1 - Coffee Stock AI Analyzer

## Overview
This repository contains the Coffee Stock AI Analyzer — an AI-powered full-stack dashboard developed to simulate inventory intelligence for a gourmet coffee shop. The application helps business owners monitor inventory, analyze historical sales, and receive smart stock recommendations through AI.

## Repository Structure

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

## Core Components

### Backend — FastAPI REST API (backend/)
A robust data layer that manages inventory and integrates with Generative AI.

Features

Inventory Management: CRUD operations for coffee shop products.

Data Simulation: Scripts to generate realistic sales and waste trends.

AI Integration: Integration with Groq API (Llama 3.3) to generate inventory advice.

ORM Layer: SQLite database using SQLModel.

Swagger UI: Interactive API documentation.

### Frontend — React Dashboard (frontend/)
A modern UI for real-time inventory monitoring.

Concepts covered:

State Management: useState for product and analysis data.

Tailwind CSS: Responsive and modern UI.

Async Actions: Fetching backend data and triggering AI analysis.

Data Visualization: Showing stock levels and AI results.

## Tech Stack

Frontend: React 18, Vite, Tailwind CSS  
Backend: Python, FastAPI, SQLModel  
Database: SQLite  
AI Engine: Groq API (Llama 3.3)

## Quick Start

### Backend

cd backend  
python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  
python init_db.py  
python seed_sales.py  
python seed_waste.py  
uvicorn main:app --reload  

Backend runs at: http://localhost:8000  
Docs: http://localhost:8000/docs  

### Frontend

cd frontend  
npm install  
npm run dev  

Frontend runs at: http://localhost:5173  

## Environment Variables

Create a .env file inside backend:

GROQ_API_KEY=your_api_key_here  

## Business Logic & AI

The system solves the overstock vs understock problem.

By analyzing stock and daily sales, it gives recommendations like:

Increase order due to high demand.  
Avoid restocking due to low sales.  

## Project Architecture

Frontend (React)  
↓  
Backend (FastAPI)  
↓  
Database (SQLite)  
↓  
AI Service (Groq)

## API Endpoints

GET /api/products → list products  
GET /api/ai/analyze/{id} → AI analysis  

## Team Responsibilities

Database Engineer → Database design & simulation  
AI Engineer → AI integration  
Backend Developer → API & logic  
Frontend Developer → UI  
Integration Engineer → System connection  

## Course Context

This project demonstrates:

REST API design  
database modeling  
ORM usage  
frontend-backend integration  
AI integration   generative AI integration
