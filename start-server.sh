#!/bin/bash

# Boeing AI Summary Server Startup Script

echo "🚀 Starting Boeing AI Summary Server..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found! Please make sure your OpenAI API key is in the .env file"
    exit 1
fi

# Check if OpenAI API key is set
if ! grep -q "OPENAI_API_KEY=" .env; then
    echo "❌ OPENAI_API_KEY not found in .env file"
    exit 1
fi

echo "✅ All checks passed!"
echo "🏃 Starting server on port 3001..."
echo "📊 Your Boeing analysis will be available with AI summaries!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
npm start