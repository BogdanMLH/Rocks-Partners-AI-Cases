# 🚀 AI Automation Operations - Proof of Concept
**Showcase repository for Rocks Partners Ecosystem**

This repository contains two MVP projects demonstrating an approach to integrating AI into real-world iGaming business processes. The primary goal of these projects is to showcase the transition from "AI as a simple chatbot" to "AI as the operational layer of a company."

## 📂 Project 1: Predictive Churn & Automated Retention Pipeline
An end-to-end architecture for automated player churn prediction and retention.

* **Problem:** Managers physically lack the time to track the churn risk of thousands of players and manually generate personalized retention offers.
* **Solution:** 1. An ML model (`Scikit-learn`), trained on historical data, predicts the probability of player churn (Churn Risk).
  2. A `FastAPI` microservice wraps the model and handles prediction requests.
  3. `n8n` orchestrates the workflow: it fetches mock player data, pings the API, and if the churn risk is >= 35%, forwards the player profile to the LLM.
  4. The LLM generates a highly personalized retention offer (e.g., free spins based on the player's LTV).
  5. An alert is instantly sent to the VIP manager via Telegram, and the data is logged into Google Sheets for analytics.
* **Tech Stack:** Python, FastAPI, n8n, Scikit-learn, OpenAI API, Telegram API.

## 📂 Project 2: AI Support Router (Smart Ticketing)
An interactive AI support assistant with incident routing logic. Demonstration based on the Baloo.bet brand.

* **Problem:** First-line support is often overloaded with basic FAQ inquiries, increasing the risk that critical requests (e.g., Responsible Gaming) get lost in the queue.
* **Solution:**
  1. A frontend chat interface sends user requests via Webhook to `n8n`.
  2. An LLM node equipped with a knowledge base (FAQ Tool) analyzes the customer's intent.
  3. The LLM returns a structured JSON object containing Category, Urgency, and the Reply Text.
  4. Automated routing: basic questions receive an instant AI reply on the frontend, while toxic requests, account deletion inquiries, or high-risk issues (High Urgency) are immediately escalated to a human manager in Telegram.
* **Tech Stack:** HTML/JS/CSS, n8n, OpenAI API (Structured Output).

---
*Developed over the weekend as an architectural proof of concept.*