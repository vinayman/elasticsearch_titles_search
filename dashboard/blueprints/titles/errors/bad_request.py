class BadRequest(Exception):
    status_code = 400

    def __init__(self, message, details=None):
        Exception.__init__(self)
        self.message = message
        self.details = details if details is not None else dict()

    def to_dict(self):
        return dict(
            code=BadRequest.status_code,
            message=self.message,
            details=self.details,
        )
