from .automation import EmailMessage, build_case_payload


def main() -> None:
    message = EmailMessage(
        subject="Urgent claim document received",
        body="Please create a case from claim number CLM-4471 with the attached document.",
        attachments=["claim.pdf"],
        sender="member@example.com",
        message_id="msg-demo-001",
    )
    print(build_case_payload(message))


if __name__ == "__main__":
    main()
