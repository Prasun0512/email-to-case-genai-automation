# Production Readiness

## Deployment

- Run ingestion and extraction as separate workers behind a queue.
- Store raw emails and attachments in encrypted object storage.
- Use idempotency keys based on message IDs before creating cases.

## Security

- Redact sensitive fields before logging.
- Keep Graph API, storage, queue, and case API credentials in a secret manager.
- Restrict case creation to validated payloads.

## Monitoring

- Track ingestion failures, extraction confidence, review rate, DLQ depth, and case API latency.
- Alert when high-priority review backlog grows.

## Cost Optimization

- Use deterministic extraction before invoking LLMs.
- Route only ambiguous attachments to premium models.
- Cache OCR output by artifact checksum.

## Scalability

- Use Service Bus partitions for high-volume inboxes.
- Process attachments asynchronously.
- Separate low-priority and high-priority queues when required.
