"""Unit tests for LangGraph state machine structure and nodes."""
import unittest
from agent.graph import build_graph


class TestGraph(unittest.TestCase):
    def test_build_graph(self):
        graph = build_graph()
        self.assertIsNotNone(graph)
        # Verify node existence
        nodes = graph.get_graph().nodes
        self.assertIn("intro", nodes)
        self.assertIn("ask_question", nodes)
        self.assertIn("analyse_requirements", nodes)
        self.assertIn("generate_user_stories", nodes)
        self.assertIn("validate", nodes)
        self.assertIn("validate_deliverables", nodes)
        self.assertIn("handoff", nodes)


if __name__ == "__main__":
    unittest.main()
