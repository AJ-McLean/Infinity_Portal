# Boeing AI Summary Feature

## Overview
This feature adds AI-powered summaries to your Boeing stock analysis tool, providing contextual insights about the most impactful tweets during selected time periods.

## Features
- 🤖 **AI-Generated Summaries**: Uses GPT-4 to analyze top tweets and generate narrative summaries
- 🔒 **Secure Backend**: API keys are safely stored on the server, never exposed to frontend
- ⚡ **Real-time Updates**: Summaries automatically generate when you change time windows
- 📊 **Context-Aware**: Focuses on highest impression tweets for maximum impact analysis

## Quick Start

### 1. Start the Backend Server
```bash
./start-server.sh
```

Or manually:
```bash
npm install
npm start
```

### 2. Open Your Analysis Tool
Open `boeing_stock_topics_hd.html` in your browser

### 3. Use the Feature
- Use the range slider under the stock chart to select a time period
- The AI summary will automatically appear between the charts and topics table
- Click and drag the range slider to analyze different periods

## How It Works

### Architecture
```
Frontend (HTML) → Backend Server (Port 3001) → OpenAI API
```

### Data Flow
1. User selects time window on frontend
2. Frontend filters tweets for that period
3. Backend receives tweets and calls OpenAI API securely
4. GPT-4 analyzes top impression tweets
5. Summary is returned and displayed to user

### Security
- ✅ API key stored in `.env` file on server
- ✅ No sensitive data exposed to frontend
- ✅ CORS enabled for local development
- ✅ Request validation and error handling

## Files Created/Modified

### New Files
- `summary-server.js` - Express backend server
- `package.json` - Node.js dependencies
- `start-server.sh` - Startup script
- `README-AI-Summary.md` - This documentation

### Modified Files
- `boeing_stock_topics_hd.html` - Added AI summary UI and backend integration

## Troubleshooting

### Server Won't Start
- Check that Node.js is installed
- Verify `.env` file contains `OPENAI_API_KEY`
- Make sure port 3001 is available

### No Summary Generated  
- Check browser console for errors
- Verify backend server is running on port 3001
- Test health endpoint: `curl http://localhost:3001/health`

### API Key Issues
- Ensure `.env` file exists in project root
- Verify API key format: `OPENAI_API_KEY=sk-...`
- Check OpenAI account has credits available

## API Endpoints

### POST `/api/generate-summary`
Generates AI summary for provided tweets
- **Body**: `{ tweets: [...], timeWindow: "date range" }`
- **Response**: `{ success: true, summary: "...", tweetsAnalyzed: 10 }`

### GET `/health`  
Health check endpoint
- **Response**: `{ status: "OK", timestamp: "..." }`

## Development

### Running in Development Mode
```bash
npm run dev  # Uses nodemon for auto-restart
```

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
PORT=3001  # Optional, defaults to 3001
```

## Production Considerations

For production deployment:
- Use process manager like PM2
- Set up proper SSL/HTTPS
- Configure firewall rules
- Use environment-based configuration
- Add rate limiting and request validation
- Consider caching for repeated requests

---

🎉 **Your Boeing analysis tool now has AI-powered narrative summaries!**