from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jinja2 import Environment, FileSystemLoader

from config import setting

file_loader = FileSystemLoader(searchpath="templates/")
env = Environment(loader=file_loader, auto_reload=True)


settings = setting.EmailSettings()


class Email:
    def __init__(self):
        self._email_configuration = ConnectionConfig(**settings.dict())

    async def send_email(self, subject: str, to: str, content: dict[str:str]):
        template = env.get_template("email.html")
        html = template.render(
            title=content.get("title"),
            name=content.get("name"),
            content=content.get("content"),
            endpoint_url=content.get("endpoint"),
        )
        message = MessageSchema(
            subject=subject,
            recipients=[to],
            body=html,
            subtype="html",
        )
        fm = FastMail(self._email_configuration)
        await fm.send_message(message, template_name="email.html")

    def send_email_background(
        self,
        background_task: BackgroundTasks,
        subject: str,
        content: dict[str, str],
        to: str,
    ):
        template = env.get_template("email.html")
        html = template.render(
            title=content.get("title"),
            name=content.get("name"),
            content=content.get("content"),
            endpoint_url=content.get("endpoint"),
        )
        message = MessageSchema(
            subject=subject,
            recipients=[to],
            body=html,
            subtype="html",
        )
        fm = FastMail(self._email_configuration)
        background_task.add_task(fm.send_message, message, template_name="email.html")
