from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
CLAIM_RE = re.compile(
    r"\b(?:claim|policy|member|invoice)[ -]?(?:id|number|no)[:# ]+([A-Z0-9-]{4,})\b",
    re.I,
)


@dataclass(frozen=True)
class EmailMessage:
    subject: str
    body: str
    attachments: list[str] = field(default_factory=list)
    sender: str = "unknown@example.com"
    message_id: str = ""


@dataclass(frozen=True)
class CasePayload:
    title: str
    category: str
    priority: str
    confidence: float
    requires_review: bool
    case_key: str = ""
    requester: str = "unknown"
    extracted_fields: dict[str, str] = field(default_factory=dict)
    validation_errors: list[str] = field(default_factory=list)
    audit: list[str] = field(default_factory=list)


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def classify_email(message: EmailMessage) -> tuple[str, str]:
    text = f"{message.subject} {message.body}".lower()
    if any(term in text for term in ("claim", "policy", "invoice", "reimbursement")):
        category = "claims"
    elif any(term in text for term in ("password", "access", "login", "support")):
        category = "support"
    else:
        category = "general"

    priority = "high" if any(term in text for term in ("urgent", "escalation", "blocked")) else "normal"
    return category, priority


def extract_case_fields(message: EmailMessage) -> dict[str, str]:
    text = normalize_text(f"{message.subject} {message.body}")
    requester_match = EMAIL_RE.search(message.sender) or EMAIL_RE.search(text)
    claim_match = CLAIM_RE.search(text)
    fields = {
        "requester": requester_match.group(0) if requester_match else "unknown",
        "summary": text[:220],
        "attachment_count": str(len(message.attachments)),
    }
    if claim_match:
        fields["reference_id"] = claim_match.group(1).upper()
    if message.attachments:
        fields["artifact_location"] = "blob://inbound-email-artifacts/"
    return fields


def build_idempotency_key(message: EmailMessage) -> str:
    source = message.message_id or f"{message.sender}:{message.subject}:{message.body}"
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]


def score_confidence(category: str, fields: dict[str, str], attachments: list[str]) -> float:
    score = 0.45
    if category != "general":
        score += 0.18
    if fields.get("requester") != "unknown":
        score += 0.15
    if fields.get("reference_id"):
        score += 0.12
    if attachments:
        score += 0.1
    return round(min(score, 0.97), 2)


def validate_payload(category: str, fields: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if category == "general":
        errors.append("category_not_specific")
    if fields.get("requester") == "unknown":
        errors.append("requester_missing")
    if len(fields.get("summary", "")) < 20:
        errors.append("summary_too_short")
    return errors


def build_case_payload(message: EmailMessage, threshold: float = 0.8) -> CasePayload:
    category, priority = classify_email(message)
    fields = extract_case_fields(message)
    confidence = score_confidence(category, fields, message.attachments)
    errors = validate_payload(category, fields)
    requires_review = bool(errors) or confidence < threshold or priority == "high"
    audit = [
        "ingested:email",
        f"classified:{category}",
        f"priority:{priority}",
        f"confidence:{confidence}",
    ]
    if requires_review:
        audit.append("route:human_review")
    else:
        audit.append("route:case_creation_api")
    return CasePayload(
        title=normalize_text(message.subject) or "Untitled case",
        category=category,
        priority=priority,
        confidence=confidence,
        requires_review=requires_review,
        case_key=build_idempotency_key(message),
        requester=fields["requester"],
        extracted_fields=fields,
        validation_errors=errors,
        audit=audit,
    )
