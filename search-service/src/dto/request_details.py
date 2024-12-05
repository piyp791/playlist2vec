class RequestDetails:
    def __init__(self, payload):
        self.endpoint = payload["endpoint"] if "endpoint" in payload else ""
        self.requestid = payload["requestid"] if "requestid" in payload else ""

    def asdict(self) -> dict:
        return {"endpoint": self.endpoint, "requestid": self.requestid}