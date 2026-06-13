from .automation import EmailMessage, build_case_payload


def main() -> None:
    message = EmailMessage(
        subject="Urgent claim document received",
        body="Please create a case from the attached claim document.",
        attachments=["claim.pdf"],
    )
    print(build_case_payload(message))


if __name__ == "__main__":
    main()
