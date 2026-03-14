# SWE314 Web Programming Project Report 
## Coffee Stock AI Analyzer

## 1. Introduction

Inventory management is a critical challenge for small businesses such as coffee shops. Maintaining the right balance between overstocking and understocking is difficult, especially when demand patterns fluctuate. Overstocking may lead to financial loss and product waste, while understocking may result in missed sales opportunities and reduced customer satisfaction.

This project presents Coffee Stock AI Analyzer, a full-stack web application designed to simulate intelligent inventory monitoring for a gourmet coffee shop. The system combines a relational database, a REST API backend, an interactive frontend dashboard, and an AI analysis module powered by Google Gemini.

The application analyzes historical sales data and current inventory levels to generate natural language recommendations about stock management. By integrating AI with traditional inventory data analysis, the system demonstrates how modern software architectures can support smarter business decisions.

## 2. Project Objectives

The primary objectives of this project are:

- To design and implement a full-stack web application

- To demonstrate database persistence and relational modeling

- To build a RESTful backend using FastAPI

- To create a responsive dashboard interface using React

- To integrate Generative AI for decision support

- To simulate realistic business scenarios using generated datasets

Through this project, we aimed to combine multiple technologies covered in the course into a single cohesive system.

## 3. System Architecture

The system follows a standard three-layer architecture consisting of a frontend layer, a backend layer, and a data layer, with an additional AI service layer.
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
Gemini AI API
```
**Frontend Layer**

The frontend is implemented using **React and Vite**, providing a modern dashboard interface where users can view product inventory and request AI analysis.

**Backend Layer**

The backend is implemented using **FastAPI**, which exposes REST API endpoints that allow the frontend to retrieve product data and request stock analysis.

**Data Layer**

The database is implemented using **SQLite** and managed through **SQLModel**, which provides an ORM abstraction over the relational schema.

**AI Layer**

The application integrates the **Google Gemini API**, which processes structured inventory data and generates human-readable stock recommendations.

## 4. Database Design

The system uses a relational database composed of three main tables.

**Product**

The Product table stores inventory items available in the coffee shop.

Fields include:

- id – unique identifier

- name – product name

- current_stock – available inventory level

- unit – measurement unit (kg, liter, piece)

**Sale**

The Sale table stores historical sales records.

Fields include:

- id – primary key

- product_id – foreign key referencing Product

- quantity – quantity sold

- date – date of transaction

Relationship:

```bash
Product (1) → (N) Sale
```

This table allows the system to calculate average sales trends.

**Waste**

The Waste table stores records of discarded or expired inventory.

Fields include:

- id – primary key

- product_id – foreign key referencing Product

- quantity – discarded amount

- date – date of waste

- reason – reason for waste

Relationship:

```bash
Product (1) → (N) Waste
```

Tracking waste helps simulate real-world inventory inefficiencies.

## 5. Data Simulation

Since real coffee shop data was not available, the project includes scripts that generate realistic mock datasets.

**init_db.py**

Creates the database tables and inserts the initial set of inventory items.

**seed_sales.py**

Generates approximately 30 days of historical sales data, allowing the backend to compute demand trends.

**seed_waste.py**

Generates records representing product waste due to expiration or operational errors.

These scripts simulate realistic operational conditions for inventory analysis.

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

One of the most innovative components of the project is the integration of Google Gemini AI.

When a user requests analysis for a product, the system sends structured data to the AI model, including:

- product name

- current stock level

- average recent sales

The AI then generates a recommendation such as:

- increasing stock before peak demand

- avoiding unnecessary restocking

- identifying potential inventory risks

This demonstrates how Generative AI can assist decision-making in business systems.

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

The Coffee Stock AI Analyzer demonstrates how modern web technologies and AI services can be combined to create intelligent business support tools.

By integrating database design, backend APIs, frontend dashboards, and generative AI, the system simulates a realistic inventory management scenario.

This project highlights the potential of AI-assisted decision-making in small business environments and illustrates the practical application of full-stack development concepts covered in the Web Programming course.
