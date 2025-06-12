from ddd.order_management.application import ports

class LoggingService(ports.LoggingServiceAbstract):
    def log(self, message: str):
        print(f"[LOG] {message}")