from ddd.order_management.application import ports

class MyEmailSender(ports.EmailSenderAbstract):
    def send_email(self, message: str):
        print(f"email sent {message}")