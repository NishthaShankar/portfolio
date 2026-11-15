# Nishtha Shankar – Portfolio

Flask (Python) portfolio with a working **contact form** (saved to SQLite) and a **visitor counter**.

## Run locally
```bash
pip install -r requirements.txt
python app.py        # http://localhost:5000
```

## Add the other hackathon certificates
Put the images in `static/img/certs/` with these exact names – they appear automatically:
- `manipal-2026.jpg`
- `sih-2025.jpg`
- `inceptrix-2025.jpg`

## Deploy free on Render
1. Push this folder to a GitHub repo.
2. On render.com: New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Environment variables: `SECRET_KEY` (any random string), `ADMIN_KEY` (your private password).

View messages at `/admin/messages?key=YOUR_ADMIN_KEY`.

Note: Render's free tier has a temporary disk, so messages and the counter can reset when the service restarts.
