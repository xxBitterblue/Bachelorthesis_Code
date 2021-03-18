from validation.ValidationExceptions.ValidationRuleException import ValidationRuleException


class ValidationRuleVersionException(ValidationRuleException):

    def __init__(self, message="Validation Rule Version Error"):
        super(ValidationRuleVersionException, self).__init__(message)
