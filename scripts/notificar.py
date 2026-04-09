import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def _build_message(smtp_user: str, notify_email: str, status: str) -> MIMEText:
    success = status.upper() == "SUCCESS"
    subject = f"[CI/CD] Pipeline {'concluído com sucesso' if success else 'falhou'}"
    body = (
        f"O pipeline foi executado com status: {status.upper()}.\n\n"
        f"Acesse a aba Actions no GitHub para mais detalhes."
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = notify_email
    return msg


def send_notification(smtp_user: str, smtp_password: str, notify_email: str, status: str) -> None:
    msg = _build_message(smtp_user, notify_email, status)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, notify_email, msg.as_string())


def main() -> None:
    required = {
        "SMTP_USER": os.getenv("SMTP_USER"),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
        "NOTIFY_EMAIL": os.getenv("NOTIFY_EMAIL"),
        "PIPELINE_STATUS": os.getenv("PIPELINE_STATUS"),
    }

    missing = [key for key, value in required.items() if not value]
    if missing:
        raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")

    send_notification(
        smtp_user=required["SMTP_USER"],
        smtp_password=required["SMTP_PASSWORD"],
        notify_email=required["NOTIFY_EMAIL"],
        status=required["PIPELINE_STATUS"],
    )
    print(f"Notificação enviada para {required['NOTIFY_EMAIL']} com status {required['PIPELINE_STATUS']}.")


if __name__ == "__main__":
    main()
