# Machine-Efficiency-Dasboard
This is a full-stack web application that uses a PyTorch-based linear regression model to predict machine (CPU metrics) efficiency based on numerical metrics.

**Features**

Frontend: React.js

  - Accepts numeric inputs for various machine performance metrics
  
  - Displays predicted efficiency score (1 -100)

Backend: Flask (Python)

  - Two REST API endpoints
  
  - Loads and runs a PyTorch linear regression model for predictions

Machine Learning:

  - PyTorch-based linear regression model
  
  - Trained on numeric data to predict machine performance


**Backend Setup:**
  - cd backend
  - python -m venv venv (Optional for virtual enviroment)
  - source venv/bin/activate (use venv\Scripts\activate on Windows)
  - pip install -r requirements.txt
  - python config.py (starts the Flask API)
  - The backend will be hosted at: http://localhost:5000

**Frontend Setup:**
  - cd frontend
  - npm install
  - npm run dev
  - The frontend will run locally and should send requests to the backend at http://localhost:5000.
