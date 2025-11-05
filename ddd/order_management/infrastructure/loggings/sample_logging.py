from ddd.order_management.application import ports

#Protocol from porst.LoggingAbstract
class SampleLogging:
    def log(self, message: str):
        print(f"[LOG] {message}")