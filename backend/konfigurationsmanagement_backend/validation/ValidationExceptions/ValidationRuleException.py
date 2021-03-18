from rest_framework import exceptions


class ValidationRuleException(exceptions.APIException):
    status_code = 200

    def __init__(self, message="Validation Rule Error"):
        super(ValidationRuleException, self).__init__(message)
