KrishiAI – Farmer Market Connect
1. Project Overview
KrishiAI (Farmer Market Connect) is a web application built with Streamlit and HTML/CSS/JavaScript that helps farmers and buyers connect directly, browse crop listings, compare sample mandi price trends, find nearby buyers on a map, and get agricultural guidance through Krishi AI. Its main purpose is to simplify direct farm-to-buyer discovery and provide accessible, multi-language agricultural tools in a clean interface.

2. Problem Statement
Small and regional farmers often face limited direct access to buyers, difficulty comparing market prices across mandis, and language or interface barriers when using digital tools. At the same time, embedding API keys directly inside frontend HTML files exposes secrets in browser code. KrishiAI addresses these challenges by combining direct marketplace/buyer discovery, sample price trend views, multi-language support, and server-side secret handling via Streamlit.

3. Objectives
To identify and address the specified problem of connecting farmers with buyers and accessible market/farming information.

To develop an effective and user-friendly solution, including an Easy Farmer Mode and multi-language interface.

To implement relevant technologies—including Streamlit, Leaflet, and the Gemini API—to achieve the project's goals securely.

4. Technologies Used
Python (streamlit_app.py for app hosting, UI embedding, and server-side Gemini API calls)

HTML5, CSS3 & JavaScript (index.html for the frontend interface, filters, chat/enquiries, and browser localStorage state)

Streamlit (web app framework and st.secrets for secret management)

Google Gemini API (AI assistant for farming guidance, listing descriptions, and translations)

Leaflet & OpenStreetMap (interactive map and location views for nearby buyers)

Browser localStorage (client-side storage for demo/local session state)

5. Key Features
Marketplace & Listings: Browse, search, filter, and sort agricultural produce by category, location, price range, and quantity, plus add, edit, mark sold, or delete listings from the farmer view.

Nearby Buyers Map & Directory: View buyers in map or list view with distance calculation, distance/location filters, and Google Maps search/direction links.

Market Prices & Trends: Explore sample mandi price ranges and 6-week trend charts alongside multi-language support and Easy Farmer Mode.

Krishi AI & Messaging: Ask farming questions powered by Gemini configured via st.secrets, send enquiries/messages, and view notifications.

6. How to Run the Project
Clone or download the repository:

Bash
git clone https://github.com/SoumeliDey/KrishiAI.git
cd KrishiAI
Install the required dependencies:

Bash
pip install streamlit
Configure the necessary API keys:

Create a local .streamlit/secrets.toml file (do not commit this file to GitHub) and add:

Ini, TOML
GEMINI_API_KEY = "your-gemini-api-key"
Ensure DEFAULT_GEMINI_API_KEY in index.html remains empty ("") so no secret key is exposed in frontend code.

Run the main program:

Bash
streamlit run streamlit_app.py
Open the application in your browser at the local Streamlit URL and test the marketplace, nearby buyers map, market prices, and AI features.

7. Screenshots / Project Demo
Screenshots: [Add screenshots of Home, Marketplace, Nearby Buyers Map, Market Prices, and Krishi AI here]

Demo Video: [Add demo video or Streamlit Cloud app link here]

8. Team Members
Member 1 – [Soumeli Dey / Name]

Member 2 – [Name]

Member 3 – [Name]

Member 4 – [Name]

9. Future Scope
Connect live official mandi price feeds and real-time weather/advisory data instead of sample/demo data.

Replace browser localStorage with a persistent backend database and user authentication for multi-user production use.

Expand voice input/output and regional language coverage for even broader rural accessibility.

Add crop image/symptom diagnosis workflows and buyer-farmer order/logistics tracking.

10. Conclusion
KrishiAI (Farmer Market Connect) brings together crop listings, nearby buyer discovery, sample mandi price trends, multi-language support, and AI-assisted guidance in a single accessible web application. By keeping API keys in st.secrets and pairing a responsive frontend with Streamlit, the project provides a practical prototype for bridging farm-to-market communication while remaining safe to deploy.
