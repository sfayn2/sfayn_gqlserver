from ddd.order_management.application import ports

class EmailAdapter(ports.EmailAbstract):
    def send_email(self, message: str):
        print(f"email sent {message}")