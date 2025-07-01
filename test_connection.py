#!/usr/bin/env python3
"""
Quick connection test for OpenRouter
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key:
    print(f"✅ API key loaded successfully (length: {len(api_key)} chars)")
    print(f"   First 10 chars: {api_key[:10]}...")
else:
    print("❌ API key not found in .env file")
    print("   Make sure your .env file contains: OPENROUTER_API_KEY=your-key-here")

# Try a simple request
if api_key:
    import requests
    
    print("\n🔌 Testing OpenRouter API connection...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Interactive CV Test",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "google/gemini-2.5-flash",
        "messages": [
            {"role": "user", "content": "Say 'Hello! Connection successful!' if you can read this."}
        ],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ Response: {content}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")