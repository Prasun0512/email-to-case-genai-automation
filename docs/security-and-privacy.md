# Security and Privacy

This document complements `docs/security-and-governance.md`.

## Email Data Controls

- Do not commit real emails, attachments, mailbox IDs, customer names, credentials, or case-system URLs.
- Sanitize message bodies and attachment metadata before examples.
- Redact sensitive values before LLM calls, logs, and audit events.

## Access Controls

- Use least-privilege permissions for mailbox ingestion and case-system writes.
- Store secrets in Key Vault or an equivalent secret manager.
- Separate raw artifact storage from sanitized processing outputs.

## Human Review

Route ambiguous, low-confidence, or policy-sensitive events to manual validation before creating or updating cases.
