from ddd.order_management.application import ports

class EmailService(ports.EmailServiceAbstract):
    def send_email(self, message: str):
        print(f"email sent {message}")