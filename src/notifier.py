class Notifier:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def notify(self, value: float) -> None:
        if value > self.threshold:
            print(f"ALERT: Value {value} exceeded threshold {self.threshold}")
