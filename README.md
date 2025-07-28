# E-commerce Order Processing App (ecommerce-PQ)

This project is a cloud-based E-commerce Order Processing system built using **Azure serverless and AI services**.  
It demonstrates a modern full-stack workflow for processing customer orders securely and efficiently.

## Features
- **Frontend**: Responsive HTML & CSS order form.
- **Backend**: Azure Function App (Python) handling form submissions.
- **Database**: Azure SQL Database for storing orders.
- **Security**: Azure Key Vault for storing secrets (SQL credentials, API keys).
- **AI Integration**: Azure OpenAI for generating dynamic responses (LLM-powered insights).
- **Serverless Deployment**: Fully hosted on Azure with CI/CD support.
- **Tracking**: Generates unique order tracking codes.

## Tech Stack
- **Azure Function (Python)** for backend API.
- **Azure SQL Database** for data storage.
- **Azure Key Vault** for secret management.
- **Azure OpenAI** for AI/LLM integration.
- **HTML, CSS, and JavaScript** for frontend UI.

## How It Works
1. Users place an order via the frontend form.
2. The frontend calls the Azure Function API endpoint.
3. The function retrieves secrets (SQL credentials) from Azure Key Vault.
4. The function saves order details into Azure SQL Database.
5. Generates a tracking code and (optionally) uses Azure OpenAI for custom responses.
6. Returns confirmation to the user.

## Deployment
The app is deployed on **Azure App Services** (Function App) with CI/CD integration via GitHub.

---
