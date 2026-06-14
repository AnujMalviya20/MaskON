This project splits a static frontend (served on Vercel) and a Python/Flask backend (needs a server).

Recommended short paths to get a working deployment:

1) Host backend on Render / Heroku / Cloud Run / Railway
   - Use the `backend/` folder as the service root.
   - Ensure `requirements.txt` includes packages (Flask, Flask-CORS, opencv-python, numpy).
   - Use the included `backend/Dockerfile` or `backend/Procfile` for quick deploys.

2) After backend is running, get the public HTTPS URL (for example `https://mask-on-api.example.com`).

3) Update `frontend/config.json` in the repository (or during Vercel config step) to point to the backend URL:
   {
     "api_base": "https://mask-on-api.example.com"
   }

4) Deploy frontend on Vercel (static site). It will fetch `config.json` at runtime to know the backend URL.

Notes:
- Vercel cannot run the Python backend; keep backend hosted separately.
- OpenCV and opencv-python may require larger build time; using the provided Dockerfile (Python 3.11) is recommended.
- If you host the backend with HTTPS, update `config.json` to use https to avoid mixed-content issues.

Quick test locally:
- Start backend: `cd backend && python app.py`
- Serve frontend: `cd frontend && python -m http.server 8000`
- Edit `frontend/config.json` to set `http://127.0.0.1:5000` (default already set)
- Open `http://localhost:8000/live.html`
