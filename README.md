# ComplimentBot — ERC-8004 Agent

A friendly AI agent that generates personalized, uplifting compliments.

## API

### GET /
Returns agent info and endpoint docs.

### GET /health
Health check.

### POST /compliment
```json
// Request
{ "name": "Alice", "context": "loves hiking and coffee" }

// Response
{ "name": "Alice", "compliment": "Alice, the way you...", "agent": "ComplimentBot" }
```

## Deploy to Render (free tier, recommended)

1. Push this folder to a GitHub repo
2. Go to render.com → New → Web Service
3. Connect your repo
4. Add environment variable: GEMINI_API_KEY = your key
5. Deploy — you'll get a URL like `https://compliment-agent.onrender.com`

## Deploy to Railway

1. Push to GitHub
2. railway.app → New Project → Deploy from GitHub
3. Add GEMINI_API_KEY in Variables tab
4. Done

## Deploy to Replit

1. Upload files to a new Replit (Python template)
2. Add GEMINI_API_KEY in Secrets
3. Run — Replit gives you a public URL automatically

## Register on 8004scan.io

Once deployed, use your live URL in the ERC-8004 registration:
- **URI field**: `https://your-url.onrender.com`
- The registry will call GET / to verify your agent card
