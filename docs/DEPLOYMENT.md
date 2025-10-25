# Deployment Guide - Sunidhi Fashion Automation

## PHASE 3: Render Deployment (COMPLETED ✅)

### Backend Service Status
- **Service**: sunidhi-automation-backend
- **URL**: https://sunidhi-automation-backend.onrender.com
- **Status**: ✅ Deployed & Running
- **Runtime**: Python 3, Free Tier
- **Last Deploy**: October 26, 2025
- **Repository**: idealabsllp-jpg/sunidhi-automation

### What's Deployed
1. Flask REST API with webhook endpoints
2. Lead capture and qualification endpoints
3. Integration with Google Sheets for CRM
4. Integration with n8n for voice automation

### Environment Variables Configured
```
GOOGLE_SHEETS_API_KEY
N8N_WEBHOOK_URL
RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET
```

## PHASE 4: Website Deployment

### Option A: GitHub Pages (Recommended for Static Sites)
1. Go to Settings → Pages
2. Select main branch → /docs folder
3. Enable GitHub Pages
4. Website automatically deploys to: https://idealabsllp-jpg.github.io/sunidhi-automation

### Option B: Render Static Site
1. Create new Render service
2. Select "Static Site"
3. Connect GitHub repo
4. Set publish directory: `/website`
5. Deploy

## PHASE 5: Heartbeat Cron Job Setup

### Problem: Free Tier Spindown
Free tier services on Render spin down after 15 minutes of inactivity, causing 50+ second delays.

### Solution: Implement Heartbeat

**Option A: External Cron Service (EasyCron - FREE)**
1. Visit https://www.easycron.com/
2. Create new cron job
3. URL: `https://sunidhi-automation-backend.onrender.com/health`
4. Frequency: Every 10 minutes
5. This keeps your service warm

**Option B: GitHub Actions Workflow**
```yaml
name: Keep Backend Warm
on:
  schedule:
    - cron: '*/10 * * * *'
jobs:
  heartbeat:
    runs-on: ubuntu-latest
    steps:
      - name: Ping backend
        run: curl https://sunidhi-automation-backend.onrender.com/health
```

**Option C: Render Cron Job Service** (Paid)
1. Upgrade to paid tier
2. Set up internal cron job
3. Runs every 5 minutes

### Backend /health Endpoint
The backend already has a `/health` endpoint that:
- Returns 200 OK status
- Logs timestamp
- Keeps instance active

## PHASE 6: Testing & Validation

### Test Backend Endpoints

**1. Health Check**
```bash
curl https://sunidhi-automation-backend.onrender.com/health
```
Expected: `{ "status": "healthy", "timestamp": "..." }`

**2. Lead Capture Webhook**
```bash
curl -X POST https://sunidhi-automation-backend.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+91 9999999999"
  }'
```

**3. Check Logs on Render Dashboard**
- Visit: https://dashboard.render.com
- Select your service
- Go to Logs tab
- Verify webhook receipts

### Test Lead Flow
1. Visit website landing page
2. Submit lead capture form
3. Check Google Sheets for new entry
4. Verify n8n workflow triggered
5. Confirm voice call initiated

## PHASE 7: Production Setup

### Security Checklist
- [ ] Set strong environment variables
- [ ] Configure CORS for your domain
- [ ] Enable HTTPS (automatic on Render)
- [ ] Set up error logging (Sentry)
- [ ] Add rate limiting to endpoints
- [ ] Validate webhook signatures

### Monitoring Setup
1. **Render Dashboard Alerts**
   - Set up email notifications
   - Monitor CPU, memory, restarts

2. **Error Tracking (Sentry)**
   - Install sentry-sdk
   - Track errors in production

3. **Analytics**
   - Track lead conversions
   - Monitor voice call success rate
   - Analyze user behavior

## Troubleshooting

### Service Shows as "Spinning Down"
- This is normal for free tier
- Initial request takes 30-50 seconds
- Subsequent requests are fast
- Solution: Implement heartbeat cron

### Webhook Not Triggering
1. Check backend logs on Render
2. Verify n8n webhook URL in environment variables
3. Test endpoint with curl
4. Check Google Sheets API credentials

### Cold Start Performance
- Free tier: 30-50 seconds first load
- Paid tier: Instant response
- Solution: Upgrade for production or use heartbeat

## Next Steps

1. ✅ Backend deployment complete
2. Deploy website (GitHub Pages or Render)
3. Set up heartbeat cron job
4. Test all endpoints
5. Implement payment processing (Phase 4)
6. Set up monitoring (Phase 5)

## Useful Links

- [Render Dashboard](https://dashboard.render.com)
- [GitHub Repository](https://github.com/idealabsllp-jpg/sunidhi-automation)
- [n8n Workflow](https://n8n.io)
- [EasyCron Service](https://www.easycron.com)
- [Sentry Error Tracking](https://sentry.io)

## Support

For deployment issues:
1. Check Render logs
2. Verify environment variables
3. Test endpoints locally
4. Review GitHub Actions workflows
5. Contact development team
