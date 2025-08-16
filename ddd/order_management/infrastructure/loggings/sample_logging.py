from ddd.order_management.application import ports

class SampleLogging(ports.LoggingAbstract):
    def log(self, message: str):
        print(f"[LOG] {message}")