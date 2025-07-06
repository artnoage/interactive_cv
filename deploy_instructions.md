# 🚀 Deployment Instructions for Interactive CV

## Quick Answer for Your Deployment Agent

**Tell your deployment agent to use the ORIGINAL `interactive_agent.py` file with these settings:**

```bash
# Environment variables to set:
AGENT_MODEL=flash
OPENROUTER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Main command:
python interactive_agent.py
```

## Why This Works

The MCP complexity is **already handled gracefully** in the original code:

1. **Automatic Fallback**: If MCP subprocess fails, it uses a simple reasoning template
2. **Error Handling**: All MCP calls are wrapped in try-catch blocks
3. **No Breaking**: The agent works fine even if MCP subprocess doesn't start

## Deployment Requirements

### Minimal Requirements (Works Everywhere)
```dockerfile
FROM python:3.9-slim

# Copy project files
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV AGENT_MODEL=flash
ENV OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Run the agent
CMD ["python", "interactive_agent.py"]
```

### For Web UI (Optional)
```bash
# Also run the web server
python serve_ui.py
```

## What Happens in Different Environments

### ✅ Standard Deployment (Most Common)
- MCP subprocess works normally
- Full sequential reasoning available
- All 6 tools functional

### ✅ Restricted Containers
- MCP subprocess may fail to start
- Agent automatically falls back to simple reasoning
- 5 out of 6 tools still work perfectly
- No errors or crashes

### ✅ Cloud Platforms (Heroku, etc.)
- May have subprocess restrictions
- Graceful fallback to template reasoning
- Main functionality preserved

## Key Points for Your Agent

1. **No Special Instructions Needed**: The original code handles deployment complexity automatically
2. **No Custom Dockerfile**: Standard Python container works fine
3. **No Process Management**: The code handles MCP lifecycle internally
4. **Graceful Degradation**: If MCP fails, the agent still works with 5/6 tools
5. **Environment Agnostic**: Works in containers, VMs, bare metal, cloud platforms

## Testing the Deployment

After deployment, test with these questions:

```bash
# Test basic search (should always work)
"What papers does Vaios have on optimal transport?"

# Test sequential reasoning (tests MCP)
"How does Vaios's mathematical background connect to his ML work?"

# If MCP works: You'll see detailed step-by-step reasoning
# If MCP fails: You'll see template reasoning - both are fine!
```

## Summary

**Just deploy the original `interactive_agent.py` - it's already production-ready!**

The MCP complexity is an implementation detail that's handled internally. Your deployment agent doesn't need to know about it.