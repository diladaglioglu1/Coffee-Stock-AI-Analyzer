# SWE314 Web Programming Project Report  
## Coffee Stock AI Analyzer

---

## 1. Introduction

Inventory management is a critical challenge for small businesses such as coffee shops. Maintaining an optimal balance between overstocking and understocking becomes increasingly complex when demand patterns are dynamic and uncertain. Overstocking leads to financial loss and waste, while understocking results in missed sales and reduced customer satisfaction.

This project presents **Coffee Stock AI Analyzer**, a full-stack web application designed to simulate intelligent inventory monitoring for a gourmet coffee shop. The system integrates a relational database, a RESTful backend, a modern frontend dashboard, and an AI analysis module powered by the **Groq API**.

The application analyzes historical sales, waste, and procurement data to generate natural language recommendations for stock management.

---

## 2. Project Objectives

The primary objectives of this project are:

- Design and implement a full-stack web application  
- Develop a relational database with real-world entities  
- Build a RESTful API using **FastAPI**  
- Create a responsive UI using **React + Vite**  
- Integrate AI-based decision support using **Groq API**  
- Simulate realistic business workflows  

---

## 3. System Architecture

```bash
React Dashboard (Frontend)
        │
        │ HTTP Requests
        ▼
FastAPI REST API (Backend)
        │
        │ SQLModel ORM
        ▼
MySQL Database
        │
        ▼
Groq AI API
```

**Frontend Layer**

The frontend is implemented using **React and Vite**, providing a modern dashboard interface where users can view product inventory and request AI analysis.

**Backend Layer**

The backend is implemented using **FastAPI**, which exposes REST API endpoints that allow the frontend to retrieve product data and request stock analysis.

**Data Layer**

The system uses **MySQL** as a production-ready relational database, managed through **SQLModel ORM.** This layer ensures structured data storage and efficient querying.

**AI Layer**

The application integrates the **Groq API**,which processes structured inventory data and produces natural language recommendations for stock optimization.

## 4. Database Design

The database layer is designed to support real-world inventory and procurement workflows. It is implemented using **SQLModel** and **MySQL**, ensuring scalability and relational integrity.

**Core Entities**

- **Product** Stores inventory items with stock levels and units.

- **Sale** Tracks historical sales transactions for demand analysis.

- **Waste** Records discarded or expired inventory to simulate real-world inefficiencies.

**Extended Entities**

- **Supplier** Stores supplier information and contact details.

- **PurchaseOrder** Represents procurement orders placed to suppliers.

- **PurchaseOrderItem** Tracks individual products within each purchase order.

**Relationships**

Product (1) → (N) Sale  
Product (1) → (N) Waste  
Supplier (1) → (N) PurchaseOrder  
PurchaseOrder (1) → (N) PurchaseOrderItem  
Product (1) → (N) PurchaseOrderItem

This design enables:

- demand analysis (via Sales)

- loss tracking (via Waste)

- supply chain simulation (via Suppliers & Orders)

The schema follows normalization principles to reduce redundancy and ensure data consistency.

## 6. Backend Implementation

The backend is implemented using FastAPI, a modern Python framework designed for building high-performance APIs.

The backend provides endpoints such as:

GET /api/products
Returns the current product inventory.

GET /api/analyze/{product_id}
Performs stock analysis and generates AI recommendations.

The backend retrieves sales data from the database, calculates statistical indicators such as average sales velocity, and forwards this information to the Gemini AI module.

## 7. Frontend Implementation

The frontend dashboard is implemented using React, a JavaScript library for building dynamic user interfaces.

The dashboard allows users to:

- view current inventory levels

- trigger AI-based analysis

- receive intelligent stock recommendations

Key frontend concepts used include:

- state management using React hooks

- asynchronous data fetching from backend APIs

- responsive UI design using Tailwind CSS

- displaying AI-generated insights in a clear interface

## 8. AI Integration

The system integrates the Groq API for AI-driven analysis.

When analysis is requested, the system sends:

- product information

- current stock levels

- historical sales trends

- waste data

The AI generates insights such as:

- restocking recommendations

- demand predictions

- risk warnings

This demonstrates the use of generative AI in operational decision support systems.

## 9. Team Contributions

The project was completed collaboratively by a five-member team.

Each team member was responsible for a different subsystem:

- Database design and data simulation

- AI integration with Gemini API

- Backend development using FastAPI

- Frontend dashboard implementation

- System integration between components

Detailed descriptions of individual contributions are provided in the responsibilities folder.

## 10. Conclusion

The Coffee Stock AI Analyzer demonstrates how modern web technologies and AI services can be combined into an intelligent business support system.

By integrating a scalable database, a high-performance backend, a responsive frontend, and AI-powered analysis, the system simulates realistic inventory and supply chain management.

This project highlights the importance of combining data engineering, software architecture, and AI to build effective decision-support tools for modern businesses.
