# Profile System

The Profile system provides centralized profile management for the Interactive CV, ensuring all agents use consistent biographical and professional information.

## 🏗️ Architecture

```
Profile/
├── __init__.py               # Package initialization
├── profile_loader.py         # Profile loading and management system
└── README.md                 # This documentation
```

## 🎯 Core Purpose

The Profile system follows the blueprint philosophy of separating configuration from code:

- **Centralized Profile**: Single source of truth for all biographical information
- **Built-in Content**: Profile information embedded directly in the code for reliability
- **Agent Integration**: Seamless integration with the Interactive CV agent system
- **Consistent Formatting**: Standardized profile presentation across all contexts

## 🔧 ProfileLoader Class

The `ProfileLoader` class provides a unified interface for accessing profile information:

### Key Methods

```python
from Profile.profile_loader import ProfileLoader

loader = ProfileLoader()

# Get formatted system prompt for agents
agent_prompt = loader.get_agent_system_prompt()

# Get complete profile information
full_profile = loader.get_full_profile()

# Validate profile configuration
validation = loader.validate_profile_files()
```

### Features

- **Built-in Profile Content**: Comprehensive biographical information embedded in code
- **Agent-Ready Formatting**: Automatically formatted for AI agent consumption
- **Tool Usage Strategy**: Includes detailed instructions for optimal agent behavior
- **Error Handling**: Robust fallback mechanisms for missing configuration
- **Validation**: Built-in validation to ensure profile integrity

## 📋 Profile Content Structure

### 1. Core Identity
- Distinguished mathematician and ML researcher
- PhD in Applied Mathematics from University of Bath
- Postdoctoral experience across four countries

### 2. Executive Narrative
- Evolution from abstract mathematical theory to practical AI applications
- Unique position at nexus of foundational theory and practical systems
- Leadership in research supervision and cutting-edge AI development

### 3. Research Expertise
- **Mathematical Foundations**: Optimal Transport, Gradient Flows, Large Deviations
- **Machine Learning & AI**: LLMs, Diffusion Models, Neural OT, GANs, RL
- **Optimization & Control**: Risk-Sensitive Decision Making, POMDPs, Multi-agent Systems

### 4. Research Evolution
- **Phase 1**: Foundational Geometric Theory
- **Phase 2**: Dynamic & Variational Methods
- **Phase 3**: Applied Control & Decision Theory
- **Phase 4**: Computational & AI Innovation

### 5. Professional Experience
- WIAS Berlin (2021-Present & 2015-2017)
- Technical University of Berlin (2018-2020)
- Brown University (2013-2015)
- MPI Leipzig (2013)

### 6. Practical AI/ML Implementation
- LLM Training & Fine-Tuning (up to 32B parameters)
- Agentic Systems Development
- AI Reasoning Challenges (ARC-2)
- Game-Playing Agents

### 7. Personal Profile
- Spherical Profile Score: 54/60
- Core Philosophy: Mathematical rigor + computational innovation
- Languages: Greek (Native), English (Fluent), German/Spanish (Intermediate)

## 🚀 Agent Integration

### Tool Usage Strategy

The profile includes comprehensive instructions for optimal agent behavior:

1. **Always Use Tools First**: Never answer from general knowledge alone
2. **Use Multiple Tools Sequentially**: Gather comprehensive information through multiple searches
3. **Retry on Failures**: Use alternative search terms and different tools
4. **Build Comprehensive Answers**: Use 2-4 tools per query for rich responses
5. **Be Specific**: Reference actual papers, dates, quotes, and findings

### Agent System Prompt

The profile automatically generates a complete system prompt including:
- Full biographical information
- Research expertise keywords
- Professional experience timeline
- Tool usage instructions
- Search strategy guidelines

## 🔍 Validation and Testing

### Profile Validation

```python
validation = loader.validate_profile_files()
print(validation)
# {
#     'profile_built_in': True,
#     'agent_prompt_loaded': True,
#     'files_readable': True,
#     'issues': []
# }
```

### Testing

```bash
# Test profile loader
python Profile/profile_loader.py

# Expected output:
# ✅ Profile loader working correctly with built-in content!
```

## 🎨 Design Philosophy

### Built-in vs External Configuration

The Profile system uses **built-in content** rather than external files because:

1. **Reliability**: No dependency on external file system
2. **Deployment**: Works in any environment without file setup
3. **Version Control**: Profile changes tracked in code
4. **Consistency**: No risk of file corruption or missing files

### Blueprint Alignment

The Profile system follows the same principles as the blueprints system:
- **Separation of Concerns**: Profile data separate from business logic
- **Centralized Management**: Single source of truth
- **Validation**: Built-in validation and error handling
- **Extensibility**: Easy to modify and extend

## 🔧 Configuration and Customization

### Updating Profile Information

To update profile information:

1. Edit the `prompt_content` in `ProfileLoader._load_agent_prompt()`
2. Maintain the structured format with numbered sections
3. Update tool usage instructions if needed
4. Test with `python Profile/profile_loader.py`

### Adding New Profile Sections

```python
# Add new sections to the prompt_content string
prompt_content = """### **Agent System Prompt: My Profile**

**1. Core Identity**
...existing content...

**9. New Section**
New content here...
"""
```

## 🚀 Integration Points

### Interactive Agent System

The Profile system integrates seamlessly with:

- **`interactive_agent.py`**: Loads profile for agent system prompt
- **Search Tools**: Provides context for database searches
- **Response Generation**: Ensures consistent voice and perspective
- **Tool Instructions**: Guides optimal tool usage patterns

### Database Integration

Profile information complements database content:
- **Academic Papers**: Profile provides context for research trajectory
- **Personal Notes**: Profile explains professional evolution
- **Entity Relationships**: Profile clarifies connections and expertise

## 📈 Benefits

1. **Consistency**: All agents use identical profile information
2. **Reliability**: Built-in content eliminates file dependency issues
3. **Maintenance**: Single location for all profile updates
4. **Integration**: Seamless agent system integration
5. **Validation**: Built-in error checking and validation
6. **Deployment**: Works in any environment without setup

## 🔧 Troubleshooting

### Common Issues

**Profile not loading**: Check `ProfileLoader._load_agent_prompt()` method
**Validation failures**: Run `python Profile/profile_loader.py` for diagnostics
**Agent integration issues**: Verify agent system prompt generation
**Content formatting**: Ensure proper markdown formatting in profile content

### Debug Commands

```bash
# Test profile loader
python Profile/profile_loader.py

# Check validation
python -c "from Profile.profile_loader import ProfileLoader; loader = ProfileLoader(); print(loader.validate_profile_files())"

# View agent prompt
python -c "from Profile.profile_loader import ProfileLoader; loader = ProfileLoader(); print(loader.get_agent_system_prompt()[:500])"
```

## 📚 Related Documentation

- **Agent System**: `interactive_agent.py`
- **Database**: `DB/README.md`
- **Blueprints**: `blueprints/README.md`
- **Main Documentation**: `CLAUDE.md`

The Profile system ensures that the Interactive CV maintains a consistent, professional, and comprehensive representation of Vaios Laschos across all interactions and contexts.