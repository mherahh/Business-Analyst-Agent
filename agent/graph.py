"""LangGraph workflow definition for the Business Analyst Agent."""
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from agent.state import State
from agent import nodes
from agent.routing import (
    route_after_evaluate,
    route_after_store,
    route_after_features,
    route_after_theme,
    route_after_logo,
    route_after_confirm,
    route_after_validate,
    route_after_review,
    WRITERS,
)


def build_graph():
    """Constructs and compiles the complete LangGraph StateGraph with checkpointing."""
    g = StateGraph(State)
    node_names = [
        "intro",
        "ask_question",
        "evaluate_answer",
        "ask_followup",
        "store_answer",
        "suggest_features",
        "present_themes",
        "custom_colors",
        "present_logo_styles",
        "generate_logos",
        "pick_logo",
        "confirm_summary",
        "build_requirements_json",
        "analyse_requirements",
        "generate_user_stories",
        "generate_acceptance_criteria",
        "validate",
        "review_stories",
        "write_requirements_json",
        "write_analysis_doc",
        "write_prd",
        "write_stories_doc",
        "validate_deliverables",
        "handoff",
    ]
    for name in node_names:
        g.add_node(name, getattr(nodes, name))

    # Phase 1: Requirements Elicitation
    g.add_edge(START, "intro")
    g.add_edge("intro", "ask_question")
    g.add_edge("ask_question", "evaluate_answer")
    g.add_conditional_edges(
        "evaluate_answer",
        route_after_evaluate,
        ["ask_followup", "store_answer"],
    )
    g.add_edge("ask_followup", "evaluate_answer")
    g.add_conditional_edges(
        "store_answer",
        route_after_store,
        ["confirm_summary", "suggest_features", "ask_question", "present_themes"],
    )
    g.add_conditional_edges(
        "suggest_features",
        route_after_features,
        ["ask_question", "present_themes"],
    )

    # Phase 2: Branding & UI Design
    g.add_conditional_edges(
        "present_themes",
        route_after_theme,
        ["custom_colors", "present_logo_styles"],
    )
    g.add_edge("custom_colors", "present_logo_styles")
    g.add_edge("present_logo_styles", "generate_logos")
    g.add_edge("generate_logos", "pick_logo")
    g.add_conditional_edges(
        "pick_logo",
        route_after_logo,
        ["present_logo_styles", "confirm_summary"],
    )

    # Phase 3: Project Summary Confirmation
    g.add_conditional_edges(
        "confirm_summary",
        route_after_confirm,
        [
            "build_requirements_json",
            "present_themes",
            "present_logo_styles",
            "ask_question",
            "confirm_summary",
        ],
    )

    # Phase 4: Business Analysis, Agile Stories, Criteria & Validation Loop
    g.add_edge("build_requirements_json", "analyse_requirements")
    g.add_edge("analyse_requirements", "generate_user_stories")
    g.add_edge("generate_user_stories", "generate_acceptance_criteria")
    g.add_edge("generate_acceptance_criteria", "validate")
    g.add_conditional_edges(
        "validate",
        route_after_validate,
        [
            "analyse_requirements",
            "generate_user_stories",
            "generate_acceptance_criteria",
            "review_stories",
        ],
    )

    # Phase 5: Client Interactive Review
    g.add_conditional_edges(
        "review_stories",
        route_after_review,
        WRITERS + ["generate_user_stories", "generate_acceptance_criteria", "review_stories"],
    )

    # Phase 6: Parallel Document Generation Fan-In -> QA Deliverables Validation -> Handoff
    g.add_edge(WRITERS, "validate_deliverables")
    g.add_edge("validate_deliverables", "handoff")
    g.add_edge("handoff", END)

    return g.compile(checkpointer=MemorySaver())
