# AI Business Analyst Agent

An enterprise-grad, agentic AI Business Analyst built with **LangChain**, **LangGraph**, and **Retrieval-Augmented Generation (RAG)** over persistent vector databases (**ChromaDB**).

The agent acts as an autonomous Senior Business Analyst and Product Manager: it conducts interactive stakeholder elicitation, discovers missing features, styles project branding, grounds technical requirements using domain knowledge bases, generates agile user stories with Gherkin acceptance criteria, validates full traceability, and exports production-ready documents in both **Word (.docx)** and **Markdown (.md)** formats alongside machine-readable JSON contracts.

---

## Architecture Overview

```mermaid
flowchart TD
    START([Start]) --> Intro[Initialize Run & State]
    Intro --> Elicitation[Interactive Q&A Elicitation]
    Elicitation --> EvalAnswer{Evaluate Clarity}
    EvalAnswer -- Vague --> Followup[Clarifying Question]
    Followup --> EvalAnswer
    EvalAnswer -- Clear --> StoreAnswer[Store Answer]
    StoreAnswer --> FeatureDiscovery[Suggest Missing Features]
    FeatureDiscovery --> UIBranding[Theme & SVG Logo Selection]
    UIBranding --> SummaryConfirm{Client Confirmation}
    SummaryConfirm -- Edit --> Elicitation
    SummaryConfirm -- Approved --> RAG[RAG Retrieval from ChromaDB]
    
    subgraph Analysis & Agile Engineering
        RAG --> Analysis[Structured Requirements Analysis]
        Analysis --> Stories[Generate INVEST User Stories]
        Stories --> Criteria[Generate Gherkin Acceptance Criteria]
        Criteria --> ValidateQA{Traceability & Gap Validation}
        ValidateQA -- Gaps Found --> Analysis
        ValidateQA -- Verified --> ClientReview{Human-in-the-Loop Review}
        ClientReview -- Revise --> Stories
    end

    subgraph Parallel Deliverables Generation
        ClientReview -- Approved --> W1[write_requirements_json]
        ClientReview -- Approved --> W2[write_analysis_doc: .docx & .md]
        ClientReview -- Approved --> W3[write_prd: .docx & .md]
        ClientReview -- Approved --> W4[write_stories_doc: .docx & .md]
    end

    W1 --> QA[Quality Assurance & Traceability Matrix]
    W2 --> QA
    W3 --> QA
    W4 --> QA
    QA --> Handoff[Handoff & Artifact Manifest]
    Handoff --> END([Complete])
```

---

## Key Features

- **LangGraph State Machine Orchestration**: Deterministic multi-step agent workflow with checkpoints, conditional branching, human-in-the-loop interrupts (`langgraph.types.interrupt`), and automated repair loops.
- **Retrieval-Augmented Generation (RAG)**: Integrates persistent **ChromaDB** vector storage with semantic search over domain knowledge documents (e.g. e-commerce patterns, ISO/IEC 25010 software quality standards, MoSCoW prioritization).
- **Flexible Embedding Options**:
  - **Local Offline Embeddings**: Fast, air-gapped `sentence-transformers/all-MiniLM-L6-v2` via `langchain-huggingface` with local file resolution.
  - **Cloud Embeddings**: Google Gemini `models/text-embedding-004` via `langchain-google-genai`.
- **Multi-Provider LLM Support**: Supports **Google Gemini** (`gemini-2.5-flash`, etc.) and **OpenRouter** (`gpt-4o-mini`, `claude-3-5`, `llama-3`, etc.) with bounded JSON parsing retries.
- **Knowledge Base Deduplication**: Manifest-driven SHA256 document hashing and deterministic chunk IDs (`source::index::hash`) ensure repeat ingestion performs zero redundant embedding calls.
- **Complete Requirements Traceability (RTM)**: Formally verifies that every client feature maps to Functional Requirements (`FR-xx`), every FR maps to User Stories (`US-xx`), and every User Story has testable Gherkin Acceptance Criteria (`AC-xx`).
- **Dual-Format Artifact Publishing**: Simultaneously exports styled Microsoft Word (`.docx`) documents and clean GitHub-flavored Markdown (`.md`) files.

---

## Project Structure

```
BusinessAnalyst-Agent/
├── agent/                        # LangGraph workflow orchestration
│   ├── graph.py                  # StateGraph definition and node edge wiring
│   ├── nodes.py                  # Atomic workflow nodes (elicitation, RAG, docs, QA)
│   ├── routing.py                # Conditional routing and input parsing helpers
│   └── state.py                  # TypedDict shared graph state schema
├── config/                       # Configuration and constants
│   ├── constants.py              # Elicitation questions, color presets, logo styles
│   └── settings.py               # Paths, RAG parameters, environment settings
├── knowledge_base/               # Raw markdown/pdf/docx domain guidance files
│   ├── business_analysis_standards.md   # ISO 25010, MoSCoW, INVEST, Gherkin guide
│   └── sample_ecommerce_best_practices.md # E-commerce architecture best practices
├── services/                     # Reusable modular services
│   ├── document_ingestion_service.py # Multi-format document parser & text chunker
│   ├── document_service.py       # Styled Word (.docx) & Markdown (.md) generator
│   ├── embedding_service.py      # Local HuggingFace & Gemini embeddings abstraction
│   ├── llm_service.py            # Gemini & OpenRouter LLM clients with JSON retries
│   ├── retrieval_service.py      # RAG orchestration and similarity query layer
│   └── vector_store_service.py   # ChromaDB wrapper with manifest-based dedup
├── scripts/                      # Operational scripts
│   └── ingest_knowledge_base.py  # Standalone CLI knowledge base ingestion script
├── tests/                        # Comprehensive automated unit test suite
│   ├── test_document_ingestion.py
│   ├── test_document_service.py
│   ├── test_graph.py
│   └── test_routing.py
├── outputs/                      # Isolated run deliverables
│   └── runs/<run_id>/            # Per-run generated deliverables
├── main.py                       # Application CLI entry point
├── requirements.txt              # Production dependency specifications
├── .env.example                  # Environment configuration template
└── README.md                     # Repository documentation
```

---

## Getting Started

### 1. Prerequisites
- **Python 3.10 to 3.13** installed.

### 2. Installation
Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/your-username/BusinessAnalyst-Agent.git
cd BusinessAnalyst-Agent

python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Configure your preferred LLM provider in `.env`:

**Option A: Using OpenRouter (Default)**
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini

EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Option B: Using Google Gemini**
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

EMBEDDING_PROVIDER=local  # or 'gemini'
```

---

## Usage

### Ingest Domain Knowledge Base
Embed and index reference documents from `knowledge_base/` into ChromaDB:

```bash
python scripts/ingest_knowledge_base.py
```

### Run Interactive Business Analyst Agent
Start the interactive requirements elicitation session in your terminal:

```bash
python main.py
```

### Run Automated End-to-End Demo
To verify the entire pipeline automatically without manual typing:

```bash
python main.py --demo
```

### Run Unit Tests
Execute the automated test suite covering chunking, routing, document exports, and graph compilation:

```bash
python -m unittest discover -s tests
```

---

## Generated Deliverables

Each agent execution creates an isolated run directory under `outputs/runs/<project_timestamp_id>/` containing:

| Deliverable | Formats | Purpose |
|---|---|---|
| **Product Requirements Document (PRD)** | `.docx`, `.md` | Executive summary, branding, product goals, core functional scope |
| **Business Requirement Analysis** | `.docx`, `.md` | Objectives, personas, FRs, ISO 25010 NFRs, scope boundaries, risks |
| **Agile User Stories & Acceptance Criteria** | `.docx`, `.md` | INVEST user stories, MoSCoW priorities, Gherkin BDD criteria |
| **Requirements Traceability Matrix (RTM)** | `.docx`, `.md` | Complete end-to-end mapping from Features -> FRs -> Stories -> Criteria |
| **Engineering Handoff Contract** | `.json` (`requirements.json`) | Machine-readable handoff specification for Software Architect agents |
| **Quality Assurance Report** | `.json` (`validation_report.json`) | Automated validation metrics and verification summary |
| **Brand Identity & Logos** | `.svg` (`logo.svg`, options 1-3) | Scalable vector logo concepts adhering to selected theme colors |

---

