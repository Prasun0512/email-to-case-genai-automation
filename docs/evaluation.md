# Evaluation Strategy

Email-to-case automation must be evaluated as an event-driven workflow, not only as an extraction prompt.

## What To Evaluate

- Duplicate email/event handling through idempotency keys.
- Retry behavior and dead-letter routing.
- Attachment metadata handling.
- Field extraction and case payload validation.
- Confidence thresholds and human-review routing.
- Audit log completeness.

## Local Checks

```bash
python -m unittest discover -s tests
python -m src.demo
```

## Quality Gates

- Duplicate events must not create duplicate cases.
- Failed extraction should retry within policy and then route to DLQ or review.
- Invalid case payloads must not be sent to downstream systems.
- Low-confidence extraction must route to human validation.

## Future Improvements

- Add generated workflow trace reports.
- Add contract tests for Graph API and CRM/TrackOps adapters.
- Add latency and queue-depth simulation.
