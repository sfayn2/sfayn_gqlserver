from ddd.order_management.application import ports

class LoggingAdapter(ports.LoggingAbstract):
    def log(self, message: str):
        print(f"[LOG] {message}")