# Farmer Market Connect (Krishi AI)

A web application built with **Streamlit** and **HTML/CSS/JavaScript** that helps farmers and buyers connect directly, explore crop listings, check sample mandi price trends, locate nearby buyers, and get agricultural guidance through **Krishi AI**.

## Features

- **Marketplace:** Browse, search, filter, and sort agricultural listings by category, location, price range, and quantity.
- **Nearby Buyers:** View buyers in map or list view (powered by Leaflet) with distance filtering and Google Maps links.
- **Market Prices:** View sample mandi price ranges and 6-week price trend charts.
- **Farmer Dashboard & Product Listings:** Add, edit, mark as sold, or delete listings and manage buyer enquiries.
- **Multi-Language & Easy Farmer Mode:** Switch interface languages and toggle larger text/simplified farmer mode.
- **Krishi AI:** Ask farming questions using Gemini configured securely on the server via Streamlit Secrets.

## Project Structure

- `streamlit_app.py` — Streamlit entry point that embeds the frontend and handles server-side Gemini API calls using `st.secrets`.
- `index.html` — Frontend interface, interactive map, localization, and browser (`localStorage`) state.

## Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/SoumeliDey/KrishiAI.git](https://github.com/SoumeliDey/KrishiAI.git)
   cd KrishiAI
