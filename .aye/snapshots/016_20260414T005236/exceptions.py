"""
ActuFlow Exceptions
===================

Custom exception classes for consistent error handling across the application.
All exceptions are caught by FastAPI exception handlers and converted to
appropriate HTTP responses.
"""

from typing import Any, Optional

from fastapi import status


class ActuFlowException(Exception):
    """
    Base exception for all ActuFlow errors.
    
    All custom exceptions should inherit from this class.
    The exception handler in main.py catches these and returns
    consistent JSON error responses.
    """
    
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[dict[str, Any]] = None,
    ):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.detail)


# =============================================================================
# Authentication & Authorization Exceptions
# =============================================================================

class AuthenticationError(ActuFlowException):
    """Raised when authentication fails."""
    
    def __init__(
        self,
        detail: str = "Authentication failed",
        error_code: str = "AUTHENTICATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=error_code,
            details=details,
        )


class AuthorizationError(ActuFlowException):
    """Raised when user lacks required permissions."""
    
    def __init__(
        self,
        detail: str = "Access denied",
        error_code: str = "AUTHORIZATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code,
            details=details,
        )


class TokenExpiredError(AuthenticationError):
    """Raised when JWT token has expired."""
    
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(detail=detail, error_code="TOKEN_EXPIRED")


class InvalidTokenError(AuthenticationError):
    """Raised when JWT token is invalid."""
    
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(detail=detail, error_code="INVALID_TOKEN")


# =============================================================================
# Resource Exceptions
# =============================================================================

class NotFoundError(ActuFlowException):
    """Raised when a requested resource is not found."""
    
    def __init__(
        self,
        resource: str = "Resource",
        resource_id: Optional[str] = None,
        detail: Optional[str] = None,
    ):
        if detail is None:
            if resource_id:
                detail = f"{resource} with ID '{resource_id}' not found"
            else:
                detail = f"{resource} not found"
        
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            details={"resource": resource, "resource_id": resource_id},
        )


class AlreadyExistsError(ActuFlowException):
    """Raised when trying to create a resource that already exists."""
    
    def __init__(
        self,
        resource: str = "Resource",
        field: Optional[str] = None,
        value: Optional[str] = None,
        detail: Optional[str] = None,
    ):
        if detail is None:
            if field and value:
                detail = f"{resource} with {field} '{value}' already exists"
            else:
                detail = f"{resource} already exists"
        
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT,
            error_code="ALREADY_EXISTS",
            details={"resource": resource, "field": field, "value": value},
        )


class ConflictError(ActuFlowException):
    """Raised when an operation conflicts with current state."""
    
    def __init__(
        self,
        detail: str = "Operation conflicts with current state",
        error_code: str = "CONFLICT",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code,
            details=details,
        )


# =============================================================================
# Validation Exceptions
# =============================================================================

class ValidationError(ActuFlowException):
    """Raised when request data fails validation."""
    
    def __init__(
        self,
        detail: str = "Validation failed",
        errors: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details={"errors": errors or []},
        )


class InvalidInputError(ValidationError):
    """Raised when input data is invalid."""
    
    def __init__(
        self,
        field: str,
        message: str,
        value: Optional[Any] = None,
    ):
        super().__init__(
            detail=f"Invalid value for '{field}': {message}",
            errors=[{"field": field, "message": message, "value": value}],
        )


# =============================================================================
# Business Logic Exceptions
# =============================================================================

class BusinessRuleError(ActuFlowException):
    """Raised when a business rule is violated."""
    
    def __init__(
        self,
        detail: str,
        error_code: str = "BUSINESS_RULE_VIOLATION",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
            details=details,
        )


class InvalidStateError(BusinessRuleError):
    """Raised when an operation is invalid for the current state."""
    
    def __init__(
        self,
        resource: str,
        current_state: str,
        operation: str,
        allowed_states: Optional[list[str]] = None,
    ):
        detail = f"Cannot {operation} {resource} in '{current_state}' state"
        if allowed_states:
            detail += f". Allowed states: {', '.join(allowed_states)}"
        
        super().__init__(
            detail=detail,
            error_code="INVALID_STATE",
            details={
                "resource": resource,
                "current_state": current_state,
                "operation": operation,
                "allowed_states": allowed_states,
            },
        )


class WorkflowError(BusinessRuleError):
    """Raised when a workflow transition is invalid."""
    
    def __init__(
        self,
        detail: str,
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            detail=detail,
            error_code="WORKFLOW_ERROR",
            details=details,
        )


# =============================================================================
# Calculation Exceptions
# =============================================================================

class CalculationError(ActuFlowException):
    """Raised when an actuarial calculation fails."""
    
    def __init__(
        self,
        detail: str = "Calculation failed",
        calculation_run_id: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        details = details or {}
        if calculation_run_id:
            details["calculation_run_id"] = calculation_run_id
        
        super().__init__(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="CALCULATION_ERROR",
            details=details,
        )


class ModelConfigurationError(CalculationError):
    """Raised when model configuration is invalid."""
    
    def __init__(self, detail: str, model_id: Optional[str] = None):
        super().__init__(
            detail=detail,
            details={"model_id": model_id} if model_id else None,
        )
        self.error_code = "MODEL_CONFIGURATION_ERROR"


class AssumptionError(CalculationError):
    """Raised when assumption data is invalid or missing."""
    
    def __init__(self, detail: str, assumption_set_id: Optional[str] = None):
        super().__init__(
            detail=detail,
            details={"assumption_set_id": assumption_set_id} if assumption_set_id else None,
        )
        self.error_code = "ASSUMPTION_ERROR"


# =============================================================================
# Data Import Exceptions
# =============================================================================

class DataImportError(ActuFlowException):
    """Raised when data import fails."""
    
    def __init__(
        self,
        detail: str = "Data import failed",
        import_id: Optional[str] = None,
        row_errors: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="DATA_IMPORT_ERROR",
            details={
                "import_id": import_id,
                "row_errors": row_errors or [],
            },
        )


class FileProcessingError(DataImportError):
    """Raised when file processing fails."""
    
    def __init__(self, detail: str, file_name: Optional[str] = None):
        super().__init__(detail=detail)
        self.error_code = "FILE_PROCESSING_ERROR"
        self.details["file_name"] = file_name


class ColumnMappingError(DataImportError):
    """Raised when column mapping is invalid."""
    
    def __init__(
        self,
        detail: str,
        missing_columns: Optional[list[str]] = None,
        unmapped_columns: Optional[list[str]] = None,
    ):
        super().__init__(detail=detail)
        self.error_code = "COLUMN_MAPPING_ERROR"
        self.details["missing_columns"] = missing_columns or []
        self.details["unmapped_columns"] = unmapped_columns or []


# =============================================================================
# External Service Exceptions
# =============================================================================

class ExternalServiceError(ActuFlowException):
    """Raised when an external service call fails."""
    
    def __init__(
        self,
        service: str,
        detail: str = "External service error",
        details: Optional[dict[str, Any]] = None,
    ):
        details = details or {}
        details["service"] = service
        
        super().__init__(
            detail=f"{service}: {detail}",
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details,
        )


class AIServiceError(ExternalServiceError):
    """Raised when AI service fails."""
    
    def __init__(self, detail: str = "AI service error"):
        super().__init__(service="AI Service", detail=detail)
        self.error_code = "AI_SERVICE_ERROR"


class StorageServiceError(ExternalServiceError):
    """Raised when storage service (S3/MinIO) fails."""
    
    def __init__(self, detail: str = "Storage service error"):
        super().__init__(service="Storage Service", detail=detail)
        self.error_code = "STORAGE_SERVICE_ERROR"


class EmailServiceError(ExternalServiceError):
    """Raised when email service fails."""
    
    def __init__(self, detail: str = "Email service error"):
        super().__init__(service="Email Service", detail=detail)
        self.error_code = "EMAIL_SERVICE_ERROR"


# =============================================================================
# Rate Limiting Exceptions
# =============================================================================

class RateLimitError(ActuFlowException):
    """Raised when rate limit is exceeded."""
    
    def __init__(
        self,
        detail: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            details={"retry_after": retry_after} if retry_after else {},
        )


# =============================================================================
# Maintenance Exceptions
# =============================================================================

class ServiceUnavailableError(ActuFlowException):
    """Raised when service is temporarily unavailable."""
    
    def __init__(
        self,
        detail: str = "Service temporarily unavailable",
        retry_after: Optional[int] = None,
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="SERVICE_UNAVAILABLE",
            details={"retry_after": retry_after} if retry_after else {},
        )


class MaintenanceModeError(ServiceUnavailableError):
    """Raised when system is in maintenance mode."""
    
    def __init__(self, detail: str = "System is under maintenance"):
        super().__init__(detail=detail)
        self.error_code = "MAINTENANCE_MODE"
