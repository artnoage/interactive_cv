# Interactive CV Project Architecture

## Project Overview
This project creates an interactive CV system that analyzes academic papers to build a comprehensive professional profile. It combines mathematical research papers with AI/ML analysis to generate insights about research expertise and career trajectory.

## System Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        Papers[Academic Papers<br/>PDFs]
        CV[CV Markdown]
        Profile[Profile Analysis]
    end

    subgraph "Processing Pipeline"
        OCR[OCR Processing<br/>Extract Text]
        LLM[LLM Analysis<br/>Extract Insights]
        Analysis[Paper Analysis<br/>Generate Summaries]
    end

    subgraph "Knowledge Base"
        Transcripts[Paper Transcripts<br/>Markdown Files]
        Analyses[Analysis Documents<br/>Structured Insights]
        Guide[Analysis Guide<br/>Methodology]
    end

    subgraph "Output Generation"
        Interactive[Interactive CV<br/>Web Interface]
        Skills[Skills Matrix<br/>Competency Graph]
        Timeline[Research Timeline<br/>Evolution View]
        Network[Collaboration Network<br/>Co-author Graph]
    end

    subgraph "Chronicle System"
        Daily[Daily Notes]
        Weekly[Weekly Notes]
        Sync[Sync Scripts]
    end

    Papers --> OCR
    OCR --> LLM
    LLM --> Analysis
    Analysis --> Transcripts
    Analysis --> Analyses
    Guide --> Analysis

    Transcripts --> Interactive
    Analyses --> Interactive
    CV --> Interactive
    Profile --> Interactive

    Interactive --> Skills
    Interactive --> Timeline
    Interactive --> Network

    Daily --> Sync
    Weekly --> Sync

    style Papers fill:#f9f,stroke:#333,stroke-width:2px
    style Interactive fill:#9f9,stroke:#333,stroke-width:2px
    style LLM fill:#99f,stroke:#333,stroke-width:2px
```

## Data Flow Diagram

```mermaid
flowchart LR
    subgraph Input
        PDF[PDF Papers]
        Meta[Metadata]
    end

    subgraph Transform
        Extract[Text Extraction]
        Analyze[AI Analysis]
        Structure[Structuring]
    end

    subgraph Storage
        MD1[Transcript MDs]
        MD2[Analysis MDs]
        DB[Knowledge Graph]
    end

    subgraph Presentation
        Web[Web Interface]
        API[API Endpoints]
        Export[Export Formats]
    end

    PDF --> Extract
    Meta --> Extract
    Extract --> Analyze
    Analyze --> Structure
    Structure --> MD1
    Structure --> MD2
    MD1 --> DB
    MD2 --> DB
    DB --> Web
    DB --> API
    API --> Export

    style PDF fill:#fdd,stroke:#333,stroke-width:2px
    style Web fill:#dfd,stroke:#333,stroke-width:2px
    style DB fill:#ddf,stroke:#333,stroke-width:2px
```

## Component Interactions

```mermaid
sequenceDiagram
    participant User
    participant System
    participant OCR
    participant LLM
    participant Storage
    participant UI

    User->>System: Upload Paper PDF
    System->>OCR: Extract Text
    OCR->>System: Return Transcript
    System->>Storage: Save Transcript MD
    System->>LLM: Analyze Paper
    LLM->>System: Return Analysis
    System->>Storage: Save Analysis MD
    System->>UI: Update Interactive CV
    UI->>User: Display Results
```

## Project Goals & Implementation Ideas

### Current State
- ✅ Paper transcripts extracted via OCR
- ✅ AI analysis of papers completed
- ✅ CV and profile documents created
- ✅ Analysis methodology documented
- ⏳ Interactive interface pending

### Proposed Features

1. **Interactive Web Interface**
   - Dynamic visualization of research areas
   - Clickable paper summaries with full analysis
   - Skill competency radar charts
   - Research timeline with key contributions

2. **Knowledge Graph Visualization**
   - Network graph of research topics
   - Connection strength based on paper relationships
   - Interactive exploration of research evolution
   - Collaboration network visualization

3. **AI-Powered Features**
   - Chat interface to query research expertise
   - Automatic generation of research statements
   - Skill matching for job descriptions
   - Research impact analysis

4. **Export Capabilities**
   - Generate tailored CVs for specific positions
   - Export research portfolio as PDF
   - API for programmatic access
   - Integration with academic platforms

### Technical Implementation

```mermaid
graph TD
    subgraph Frontend
        React[React/Next.js]
        D3[D3.js Visualizations]
        Chat[Chat Interface]
    end

    subgraph Backend
        API[FastAPI/Flask]
        Vector[Vector DB<br/>Embeddings]
        Graph[Graph DB<br/>Neo4j]
    end

    subgraph AI
        Embed[Embedding Model]
        LLM2[LLM for Chat]
        RAG[RAG Pipeline]
    end

    React --> API
    D3 --> API
    Chat --> API
    API --> Vector
    API --> Graph
    API --> RAG
    RAG --> Embed
    RAG --> LLM2
    RAG --> Vector

    style React fill:#61dafb,stroke:#333,stroke-width:2px
    style API fill:#009688,stroke:#333,stroke-width:2px
    style LLM2 fill:#ff6b6b,stroke:#333,stroke-width:2px
```

### Development Roadmap

1. **Phase 1: Static Site Generation**
   - Convert markdown to static HTML
   - Basic navigation and search
   - Deploy to GitHub Pages/Netlify

2. **Phase 2: Interactive Visualizations**
   - Add D3.js research network graph
   - Implement timeline visualization
   - Create skill competency charts

3. **Phase 3: Dynamic Features**
   - Implement backend API
   - Add vector search for papers
   - Create chat interface with RAG

4. **Phase 4: Advanced Analytics**
   - Research impact metrics
   - Collaboration analysis
   - Trend identification
   - Career trajectory modeling

### Key Benefits
- **For Job Applications**: Instantly generate tailored CVs highlighting relevant research
- **For Collaboration**: Easy discovery of expertise areas and potential synergies
- **For Self-Reflection**: Visualize research evolution and identify future directions
- **For Knowledge Management**: Centralized, searchable repository of all research work