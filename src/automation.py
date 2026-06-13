from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EmailMessage:
    subject: str
    body: str
    attachments: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CasePayload:
    title: str
    category: str
    priority: str
    confidence: float
    requires_review: bool


def classify_email(message: EmailMessage) -> tuple[str, str]:
    text = f"{message.subject} {message.body}".lower()
    category = "claims" if "claim" in text else "support"
    priority = "high" if "urgent" in text or "escalation" in text else "normal"
    return category, priority


def build_case_payload(message: EmailMessage, threshold: float = 0.8) -> CasePayload:
    category, priority = classify_email(message)
    has_attachment_context = bool(message.attachments)
    confidence = 0.88 if category == "claims" and has_attachment_context else 0.68
    return CasePayload(
        title=message.subject.strip() or "Untitled case",
        category=category,
        priority=priority,
        confidence=confidence,
        requires_review=confidence < threshold,
    )
