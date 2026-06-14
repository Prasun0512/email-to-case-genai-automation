import unittest

from src.automation import EmailMessage, build_case_payload


class AutomationTests(unittest.TestCase):
    def test_claim_email_with_attachment_is_confident(self) -> None:
        payload = build_case_payload(
            EmailMessage(
                "Claim received",
                "Please process claim number CLM-4471 for member.",
                ["claim.pdf"],
                sender="member@example.com",
                message_id="msg-001",
            )
        )
        self.assertEqual(payload.category, "claims")
        self.assertFalse(payload.requires_review)
        self.assertEqual(payload.extracted_fields["reference_id"], "CLM-4471")
        self.assertEqual(payload.requester, "member@example.com")

    def test_low_context_email_routes_to_review(self) -> None:
        payload = build_case_payload(EmailMessage("Hello", "Need help", []))
        self.assertTrue(payload.requires_review)
        self.assertIn("category_not_specific", payload.validation_errors)

    def test_high_priority_email_requires_human_review(self) -> None:
        payload = build_case_payload(
            EmailMessage(
                "Urgent claim escalation",
                "Claim number CLM-9001 is blocked.",
                ["claim.pdf"],
                sender="vip@example.com",
            )
        )
        self.assertEqual(payload.priority, "high")
        self.assertTrue(payload.requires_review)


if __name__ == "__main__":
    unittest.main()
