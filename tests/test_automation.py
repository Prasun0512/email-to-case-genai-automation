import unittest

from src.automation import EmailMessage, build_case_payload


class AutomationTests(unittest.TestCase):
    def test_claim_email_with_attachment_is_confident(self) -> None:
        payload = build_case_payload(
            EmailMessage("Claim received", "Please process claim", ["claim.pdf"])
        )
        self.assertEqual(payload.category, "claims")
        self.assertFalse(payload.requires_review)

    def test_low_context_email_routes_to_review(self) -> None:
        payload = build_case_payload(EmailMessage("Hello", "Need help", []))
        self.assertTrue(payload.requires_review)


if __name__ == "__main__":
    unittest.main()
