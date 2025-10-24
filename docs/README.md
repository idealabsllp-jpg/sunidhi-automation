# Sunidhi Fashion - Automation Documentation

## Project Overview
This directory contains all documentation for the Sunidhi Fashion Automation MVP project.

## Quick Start
1. Clone the repository
2. Set up environment variables (see .env.example)
3. Install dependencies: `pip install -r backend/requirements.txt`
4. Deploy on Render using `render.yaml`

## Architecture
- **Frontend**: Static HTML website hosted on Render/GitHub Pages
- **Backend**: Flask application on Render
- **Voice AI**: OmniDimension for voice automation
- **CRM**: Google Sheets for lead management
- **Payments**: Razorpay integration for checkout

## Key Components
- `backend/app.py` - Flask application with webhooks
- `website/index.html` - Landing page for lead capture
- `cronjobs/heartbeat.py` - Keep-alive script for Render free tier
- `docs/` - Project documentation

## Deployment
To deploy:
1. Push to GitHub
2. Connect repo to Render
3. Set environment variables
4. Render auto-deploys on push

## Support
For questions or issues, contact the development team.
