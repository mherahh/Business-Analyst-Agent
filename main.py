"""Run the Business Analyst Agent in a terminal session."""
from __future__ import annotations

import argparse
import sys
from langgraph.types import Command
from agent.graph import build_graph


SAMPLE_DEMO_ANSWERS = [
    "NovaShop",                                                    # 1. Project name
    "A modern e-commerce storefront for independent fashion brands with product catalog, cart, and payment checkout", # 2. Description
    "1",                                                           # 3. Type (Online store)
    "Customers, Store Managers, Inventory Admins",                 # 4. Target Users
    "Product catalog with search and filters, Shopping cart, Secure checkout with Stripe, Order history", # 5. Main features
    "none",                                                        # 5b. Feature suggestions
    "Product catalog, Shopping cart, Secure checkout",             # 6. Must have
    "Stripe payments, SendGrid email notifications",               # 7. Integrations
    "Next.js, FastAPI, PostgreSQL",                                # 8. Tech
    "$30,000 budget, 6 weeks deadline",                            # 9. Budget/deadline
    "1",                                                           # Theme preset (Ocean Blue)
    "1",                                                           # Logo style (Minimal)
    "1",                                                           # Pick logo option 1
    "yes",                                                         # Confirm summary
    "approve",                                                     # Review stories approval
]


def run_interactive(demo_mode: bool = False):
    """Executes the interactive Business Analyst elicitation and documentation graph."""
    graph = build_graph()
    config = {"configurable": {"thread_id": "session-1"}, "recursion_limit": 100}

    demo_iter = iter(SAMPLE_DEMO_ANSWERS) if demo_mode else None

    print("\nStarting Business Analyst Agent session...")
    result = graph.invoke({"files": []}, config)

    while "__interrupt__" in result:
        ask = result["__interrupt__"][0].value
        print("\n" + ask["question"])
        options = ask.get("options", [])
        if options:
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")

        if demo_mode:
            try:
                reply = next(demo_iter)
                print(f"> [Demo Auto-Reply]: {reply}")
            except StopIteration:
                reply = "yes"
        else:
            try:
                reply = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nSession terminated by user.")
                sys.exit(0)

        result = graph.invoke(Command(resume=reply), config)

    print("\nWorkflow completed successfully.")


def main():
    parser = argparse.ArgumentParser(description="AI Business Analyst Agent CLI")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run an automated end-to-end demo session using pre-configured sample answers.",
    )
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest all knowledge base documents into the vector store before running.",
    )

    args = parser.parse_args()

    if args.ingest:
        from scripts.ingest_knowledge_base import main as run_ingest
        print("Ingesting knowledge base...")
        exit_code = run_ingest()
        if exit_code != 0:
            print("Knowledge base ingestion failed.")
            sys.exit(exit_code)

    run_interactive(demo_mode=args.demo)


if __name__ == "__main__":
    main()
