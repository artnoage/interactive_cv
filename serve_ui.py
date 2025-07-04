#!/usr/bin/env python3
"""
Simple web server for the Interactive CV UI with integrated chat endpoint.
"""

import os
import json
import sqlite3
from pathlib import Path
from flask import Flask, render_template_string, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Import the interactive agent
from interactive_agent import InteractiveCVAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the agent
agent = None

def get_agent():
    global agent
    if agent is None:
        agent = InteractiveCVAgent()
    return agent

@app.route('/')
def index():
    """Serve the main UI."""
    with open('web_ui/index.html', 'r') as f:
        return f.read()

@app.route('/favicon.ico')
def favicon():
    """Return empty favicon to avoid 404 errors."""
    return '', 204

@app.route('/knowledge_graph.json')
def knowledge_graph():
    """Serve the knowledge graph data."""
    # First check for pruned graph in web_ui folder
    pruned_kg_path = Path('web_ui/knowledge_graph.json')
    if pruned_kg_path.exists():
        with open(pruned_kg_path, 'r') as f:
            return jsonify(json.load(f))
    
    # Fall back to main KG
    kg_path = Path('KG/knowledge_graph.json')
    if kg_path.exists():
        with open(kg_path, 'r') as f:
            return jsonify(json.load(f))
    else:
        # If KG doesn't exist, return empty graph
        return jsonify({"nodes": [], "links": []})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    try:
        data = request.json
        user_message = data.get('message', '')
        thread_id = data.get('thread_id', 'web-session')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        print(f"Received chat message: {user_message[:50]}...")
        
        # Get response from agent
        try:
            agent_instance = get_agent()
            print("Agent instance obtained")
            response = agent_instance.chat(user_message, thread_id)
            print(f"Agent response: {response[:50]}...")
        except Exception as agent_error:
            print(f"Agent error: {agent_error}")
            return jsonify({'error': f'Agent error: {str(agent_error)}'}), 500
        
        return jsonify({
            'response': response,
            'thread_id': thread_id
        })
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def stats():
    """Get database statistics."""
    try:
        conn = sqlite3.connect('DB/metadata.db')
        cursor = conn.cursor()
        
        # Get counts
        stats = {}
        
        # Academic papers
        cursor.execute("SELECT COUNT(*) FROM academic_documents")
        stats['papers'] = cursor.fetchone()[0]
        
        # Personal notes
        cursor.execute("SELECT COUNT(*) FROM chronicle_documents")
        stats['notes'] = cursor.fetchone()[0]
        
        # Topics
        cursor.execute("SELECT COUNT(*) FROM topics")
        stats['topics'] = cursor.fetchone()[0]
        
        # People
        cursor.execute("SELECT COUNT(*) FROM people")
        stats['people'] = cursor.fetchone()[0]
        
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Interactive CV server...")
    print("Initializing Interactive Agent...")
    try:
        # Pre-initialize the agent to check for errors
        test_agent = get_agent()
        print("✓ Interactive Agent initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing agent: {e}")
        print("Make sure OPENROUTER_API_KEY is set in .env file")
    
    print("\nServer endpoints:")
    print("  - Main UI: http://localhost:8888")
    print("  - Chat API: http://localhost:8888/api/chat")
    print("  - Stats API: http://localhost:8888/api/stats")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=8888, debug=True)