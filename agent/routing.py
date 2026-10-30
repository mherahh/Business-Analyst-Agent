"""Routing helpers and conditional transition logic for the LangGraph workflow."""
import re
from config.constants import QUESTIONS, WRITERS


def pick_number(reply: str, count: int) -> int | None:
    """Parses a 1-based index (e.g. '2', '2.', '2)', '#2') into a 0-based integer.

    Returns None if the reply is not a valid selection in range [1, count].
    """
    if not reply or not isinstance(reply, str):
        return None
    cleaned = reply.strip()
    m = re.match(r"^#?(\d+)[.)]?$", cleaned)
    if m:
        val = int(m.group(1))
        if 1 <= val <= count:
            return val - 1
    return None


def match_option(reply: str, options: list[str]) -> int | None:
    """Matches user input by numeric index or case-insensitive prefix/equality."""
    num_idx = pick_number(reply, len(options))
    if num_idx is not None:
        return num_idx

    cleaned = reply.strip().lower()
    for idx, opt in enumerate(options):
        opt_clean = opt.strip().lower()
        if cleaned == opt_clean or cleaned == opt_clean.split()[0]:
            return idx
    return None


def route_after_evaluate(state: dict) -> str:
    """Directs to follow-up if answer was marked vague and no follow-up was asked yet."""
    verdict = state.get("verdict", "").strip().lower()
    if verdict == "vague" and state.get("followup_count", 0) == 0:
        return "ask_followup"
    return "store_answer"


def route_after_store(state: dict) -> str:
    """Routes to feature suggestions after features question, next question, or UI theme phase."""
    if state.get("editing"):
        return "confirm_summary"
    if QUESTIONS[state["q_index"] - 1]["key"] == "features":
        return "suggest_features"
    if state["q_index"] < len(QUESTIONS):
        return "ask_question"
    return "present_themes"


def route_after_features(state: dict) -> str:
    """Proceeds to remaining questions or UI themes after feature suggestions."""
    return "ask_question" if state["q_index"] < len(QUESTIONS) else "present_themes"


def route_after_theme(state: dict) -> str:
    """Routes to custom hex entry or logo generation depending on theme choice."""
    theme_name = state.get("theme", {}).get("name", "").strip().lower()
    return "custom_colors" if theme_name == "custom" else "present_logo_styles"


def route_after_logo(state: dict) -> str:
    """Proceeds to project confirmation once a logo has been selected."""
    return "confirm_summary" if state.get("logo") else "present_logo_styles"


def route_after_confirm(state: dict) -> str:
    """Routes based on user confirmation decision (edit questions, theme, logo, or proceed)."""
    d = (state.get("decision") or "").strip().lower()
    if d in ("yes", "y", "proceed", "ok", "confirm", "continue", "looks good", "1"):
        return "build_requirements_json"
    if d in ("edit theme", "theme"):
        return "present_themes"
    if d in ("edit logo", "logo"):
        return "present_logo_styles"
    if state.get("editing"):
        return "ask_question"
    return "confirm_summary"


def route_after_validate(state: dict) -> str:
    """Directs to repair loop or onward to review_stories."""
    return state.get("next_step", "review_stories")


def route_after_review(state: dict) -> list[str] | str:
    """Parallel fan-out to all WRITERS on approval, or routes back to revise stories/criteria."""
    r = (state.get("review") or "").strip().lower()
    if r in ("approve", "approved", "yes", "y", "ok", "confirm", "proceed", "looks good", "1"):
        return WRITERS  # Returning a list runs all writer nodes in parallel in LangGraph
    if r.startswith("change stories"):
        return "generate_user_stories"
    if r.startswith("change criteria"):
        return "generate_acceptance_criteria"
    if r.startswith("change"):
        return "generate_user_stories"
    return "review_stories"
