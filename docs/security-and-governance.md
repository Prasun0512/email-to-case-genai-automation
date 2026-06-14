# Security and Governance

## Email and Attachment Safety

- Sanitize attachments before indexing or LLM processing.
- Redact sensitive identifiers from logs and examples.
- Validate attachment types and size limits.
- Quarantine unsupported or suspicious payloads.

## Workflow Governance

- Use idempotency keys to avoid duplicate case creation.
- Require human approval for low-confidence extraction or high-risk routing.
- Capture model, prompt, schema, confidence, source message ID, retry count, and final action.
- Monitor DLQ volume and recurring failure reasons.

## Secrets and Access

- Never commit mailbox credentials, API keys, case-system tokens, or connection strings.
- Use managed identity, Key Vault, and least-privilege access in production.
- Separate read access to inbound messages from write access to case systems.
