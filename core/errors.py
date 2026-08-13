class CancelInputError(Exception):
    pass

class GoBackError(Exception):
    pass

class ExtraActionSelected(Exception):
    def __init__(self, action: str, context: dict | None = None):
        self.action = action
        self.context = context or {}

class FormValidationError(Exception):
    pass