"""Shared state definition passed between LangGraph nodes in the Business Analyst workflow."""
import operator
from typing import Annotated, Any, TypedDict


class State(TypedDict, total=False):
    # Run identity and isolated output path
    run_id: str                      # Unique identifier for this run
    output_dir: str                  # Isolated output directory under outputs/runs/<run_id>

    # Quality Assurance and Traceability report
    qa_status: str                   # "passed", "warning", or "failed"
    qa_report: dict                  # Summary of feature coverage, FR count, story count, AC count

    # RAG evidence retrieved from vector store
    retrieved_evidence: list[dict]   # Knowledge base chunks retrieved for requirements analysis

    # Phase 1: Interactive requirements elicitation
    q_index: int                     # Index of current question in QUESTIONS list
    last_answer: str                 # Most recent human reply
    verdict: str                     # "clear" or "vague" from evaluate_answer
    followup_question: str           # Follow-up clarifying question if verdict is vague
    followup_count: int              # Number of follow-ups asked for current question
    answers: dict[str, str]          # Stored client answers mapped by question key
    suggested: list[str]             # Additional feature suggestions from LLM
    editing: bool                    # Flag indicating whether user is editing a prior answer

    # Phase 2: Design & UI Branding
    theme: dict[str, str]            # Color theme {"name", "primary", "background"}
    logo_style: str                  # Chosen visual style for SVG logo
    logos: list[str]                 # Generated candidate SVG logos
    logo: str                        # User's chosen final SVG logo string

    # Phase 3: Project Summary Confirmation
    decision: str                    # User decision ("yes", "edit N", "edit theme", etc.)

    # Phase 4: Business Analysis & Agile Artifact Generation
    analysis: dict[str, Any]         # Structured requirements analysis (objectives, FRs, NFRs, scope, risks)
    stories: list[dict[str, Any]]    # Agile user stories with MoSCoW priorities and FR linkages
    criteria: list[dict[str, Any]]   # Gherkin Given-When-Then acceptance criteria linked to stories
    gaps: str                        # Problems identified during validation loop
    leftover: str                    # Remaining gaps if repair attempts exceed limit
    next_step: str                   # Target node for repair loop or progression
    repairs: dict[str, int]          # Counter for repair attempts {"fr": 0, "story": 0, "criteria": 0}

    # Phase 5: Client Story Review & Feedback
    review: str                      # Client feedback or approval decision
    feedback: str                    # Human change request details if stories/criteria are revised

    # Phase 6: Deliverables Output & Handoff
    files: Annotated[list[str], operator.add]  # List of generated artifact file paths (appended across nodes)
