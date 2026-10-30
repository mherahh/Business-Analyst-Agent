"""Unit tests for agent routing and input parsing."""
import unittest
from agent.routing import pick_number, match_option, route_after_evaluate, route_after_confirm, route_after_review, WRITERS


class TestRouting(unittest.TestCase):
    def test_pick_number(self):
        self.assertEqual(pick_number("1", 5), 0)
        self.assertEqual(pick_number("2.", 5), 1)
        self.assertEqual(pick_number("3)", 5), 2)
        self.assertEqual(pick_number("#4", 5), 3)
        self.assertEqual(pick_number("5", 5), 4)
        self.assertIsNone(pick_number("0", 5))
        self.assertIsNone(pick_number("6", 5))
        self.assertIsNone(pick_number("abc", 5))
        self.assertIsNone(pick_number("", 5))

    def test_match_option(self):
        options = ["Online store", "Blog", "Portfolio", "Business site"]
        self.assertEqual(match_option("1", options), 0)
        self.assertEqual(match_option("Blog", options), 1)
        self.assertEqual(match_option("portfolio", options), 2)
        self.assertEqual(match_option("business", options), 3)

    def test_route_after_evaluate(self):
        self.assertEqual(route_after_evaluate({"verdict": "vague", "followup_count": 0}), "ask_followup")
        self.assertEqual(route_after_evaluate({"verdict": "vague", "followup_count": 1}), "store_answer")
        self.assertEqual(route_after_evaluate({"verdict": "clear", "followup_count": 0}), "store_answer")

    def test_route_after_confirm(self):
        self.assertEqual(route_after_confirm({"decision": "yes"}), "build_requirements_json")
        self.assertEqual(route_after_confirm({"decision": "y"}), "build_requirements_json")
        self.assertEqual(route_after_confirm({"decision": "PROCEED"}), "build_requirements_json")
        self.assertEqual(route_after_confirm({"decision": "edit theme"}), "present_themes")
        self.assertEqual(route_after_confirm({"decision": "edit logo"}), "present_logo_styles")
        self.assertEqual(route_after_confirm({"decision": "edit 1", "editing": True}), "ask_question")

    def test_route_after_review(self):
        self.assertEqual(route_after_review({"review": "approve"}), WRITERS)
        self.assertEqual(route_after_review({"review": "approved"}), WRITERS)
        self.assertEqual(route_after_review({"review": "yes"}), WRITERS)
        self.assertEqual(route_after_review({"review": "change stories: add guest checkout"}), "generate_user_stories")
        self.assertEqual(route_after_review({"review": "change criteria: update payment"}), "generate_acceptance_criteria")


if __name__ == "__main__":
    unittest.main()
