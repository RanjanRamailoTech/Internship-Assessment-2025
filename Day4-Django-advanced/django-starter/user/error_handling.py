from ramailo.error_handling import RamailoException

class MissingEmailError(RamailoException):
    status_code = 400
    detail = "Missing required field"
    custom_error_type = "missing_field"

    def __init__(self, message="Email is required", param="email"):
        super().__init__(message, param)
        
        
class BrokerConnectionError(RamailoException):
    status_code = 500
    detail = "Failed to connect to message broker"
    custom_error_type = "broker_error"

    def __init__(self, message="Failed to connect to message broker", param=None):
        super().__init__(message, param)
        

class ValidationError(RamailoException):
    status_code = 400
    detail = "Validation failed"
    custom_error_type = "validation_error"

    def __init__(self, message="Validation failed", param=None):
        super().__init__(message, param)
        
        
class DuplicateEmailError(RamailoException):
    status_code = 400
    detail = "Email already exists"
    custom_error_type = "duplicate_error"

    def __init__(self, message="Email already exists", param="email"):
        super().__init__(message, param)