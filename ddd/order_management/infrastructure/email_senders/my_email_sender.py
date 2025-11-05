from ddd.order_management.application import ports

# EmailSenderAbstract
class MyEmailSender:
    def send_email(self, message: str):
        print(f"email sent {message}")