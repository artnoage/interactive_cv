# Interactive CV Agent

A conversational agent that can answer questions about Vaios Laschos' research, papers, and professional journey using LangChain's AgentExecutor.

## Features

- **Multi-tool Architecture**: Uses specialized tools for different query types
- **Memory Management**: Maintains conversation history across sessions
- **Semantic Search**: Vector-based search for conceptual queries
- **Knowledge Graph Integration**: Leverages graph relationships for deeper insights
- **Real-time Streaming**: Streams responses as they're generated

## Available Tools

1. **search_academic_papers**: Find papers by topic or keywords
2. **search_chronicle_notes**: Search daily work notes and insights
3. **find_research_topics**: Discover research areas and expertise
4. **get_research_evolution**: Track how topics evolved over time
5. **find_project_connections**: Explore project relationships
6. **semantic_search**: Natural language search using embeddings
7. **get_collaborations**: Find collaboration patterns

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your `.env` file contains:
```
OPENROUTER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # For embeddings
```

3. Make sure the database is populated:
```bash
# Sync chronicle notes
./sync/sync-chronicle

# Database should already have academic papers imported
```

## Usage

### Interactive Chat Mode
```bash
python interactive_agent.py
```

Commands in chat:
- Type your question and press Enter
- `clear` - Start a new conversation
- `exit` - Quit the agent

### Test Mode
```bash
python interactive_agent.py test
```

## Example Questions

- "What papers has Vaios written about optimal transport?"
- "Show me his recent work on machine learning"
- "How has his research evolved from mathematics to AI?"
- "What projects involve reinforcement learning?"
- "What are the connections between the Interactive CV project and his research?"
- "Find papers related to GANs or neural networks"
- "What did he work on in June 2025?"

## Architecture

The agent uses LangGraph to create a stateful conversation flow:

```
User Query → Agent Node → Tool Selection → Tool Execution → Response
     ↑                                            ↓
     ←────────────── Memory & Context ←──────────←
```

### State Management
- **Messages**: Conversation history with add_messages reducer
- **Context**: Graph insights and metadata
- **Query History**: Track past queries for context

### LLM Configuration
- Model: Google Gemini 2.5 Flash (via OpenRouter)
- Temperature: 0.1 (for consistency)
- Tools: Bound dynamically based on query

## Extending the Agent

To add new tools:

1. Create a new `@tool` decorated function
2. Add it to the tools list in `agent_node` and `create_agent`
3. Ensure it returns a string (will be converted to ToolMessage)

Example:
```python
@tool
def find_mathematical_methods(area: str) -> str:
    """Find mathematical methods used in a specific area"""
    # Implementation
    return "Results as a formatted string"
```

## Troubleshooting

1. **"OPENROUTER_API_KEY not found"**: Check your `.env` file
2. **"No documents found"**: Run the sync script to populate database
3. **Tool errors**: Check that all imports are available
4. **Slow responses**: Semantic search on large databases can take time

## Performance Tips

- The agent limits context to last 10 messages to manage tokens
- Graph context is computed only for complex queries
- Tools are designed to return concise, relevant information
- Streaming provides better UX for long responses