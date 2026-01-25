const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Endpoint to generate AI summary
app.post('/api/generate-summary', async (req, res) => {
  try {
    const { tweets, timeWindow } = req.body;
    
    // Validate request
    if (!tweets || !Array.isArray(tweets) || tweets.length === 0) {
      return res.status(400).json({ 
        error: 'No tweets provided or invalid format' 
      });
    }
    
    if (!timeWindow) {
      return res.status(400).json({ 
        error: 'Time window is required' 
      });
    }
    
    // Check for OpenAI API key
    if (!process.env.OPENAI_API_KEY) {
      return res.status(500).json({ 
        error: 'OpenAI API key not configured' 
      });
    }
    
    // Get top tweets by impressions
    const topTweets = tweets
      .sort((a, b) => (b.impressions || 0) - (a.impressions || 0))
      .slice(0, 10);
    
    // Prepare tweets data for OpenAI
    const tweetsData = topTweets.map(tweet => ({
      text: tweet.snippet || tweet.text || '',
      author: tweet.author || 'Unknown',
      impressions: tweet.impressions || 0,
      date: tweet.date
    }));
    
    // Make OpenAI API call
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [{
          role: 'system',
          content: 'You are an expert financial and social media analyst. Analyze the provided tweets about Boeing and create a concise summary of the key narratives and themes during this time period. Focus on the most impactful stories and their potential market implications.'
        }, {
          role: 'user',
          content: `Please analyze these ${tweetsData.length} most impactful tweets about Boeing from ${timeWindow} and provide a concise summary of the key narratives and themes:\n\n${tweetsData.map((tweet, i) => `${i + 1}. "${tweet.text}" (${tweet.impressions.toLocaleString()} impressions, @${tweet.author})`).join('\n\n')}\n\nProvide a 2-3 paragraph summary highlighting the main themes and their potential market implications.`
        }],
        max_tokens: 500,
        temperature: 0.7
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`OpenAI API error: ${response.status} - ${errorData.error?.message || 'Unknown error'}`);
    }
    
    const data = await response.json();
    const summary = data.choices[0].message.content;
    
    // Return the summary
    res.json({
      success: true,
      summary,
      tweetsAnalyzed: tweetsData.length,
      timeWindow
    });
    
  } catch (error) {
    console.error('Error generating AI summary:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to generate summary'
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`Summary server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});