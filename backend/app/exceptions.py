"""
Custom Exceptions
=================

Application-specific exception classes.
"""

from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class ActuFlowException(Exception):
    """Base exception for ActuFlow application."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundError(ActuFlowException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            f"{resource} not found",
            {"resource": resource, "identifier": str(identifier)},
        )
        self.resource = resource
        self.identifier = identifier


class AlreadyExistsError(ActuFlowException):
    """Resource already exists."""

    def __init__(self, resource: str, field: str, value: Any):
        super().__init__(
            f"{resource} with {field}='{value}' already exists",
            {"resource": resource, "field": field, "value": str(value)},
        )


class ValidationError(ActuFlowException):
    """Validation error."""

    def __init__(self, message: str, errors: Optional[list] = None):
        super().__init__(message, {"errors": errors or []})
        self.errors = errors


class ForbiddenError(ActuFlowException):
    """Permission denied."""

    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class AuthenticationError(ActuFlowException):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class CalculationError(ActuFlowException):
    """Calculation engine error."""

    def __init__(self, message: str, calculation_id: Optional[str] = None):
        super().__init__(message, {"calculation_id": calculation_id})


class DataImportError(ActuFlowException):
    """Data import error."""

    def __init__(self, message: str, row: Optional[int] = None, column: Optional[str] = None):
        super().__init__(message, {"row": row, "column": column})


class AIServiceError(ActuFlowException):
    """AI service error."""

    def __init__(self, message: str = "AI service unavailable"):
        super().__init__(message)


class WorkflowError(ActuFlowException):
    """Workflow/state transition error."""

    def __init__(self, message: str, current_state: Optional[str] = None, target_state: Optional[str] = None):
        super().__init__(message, {"current_state": current_state, "target_state": target_state})


# =============================================================================
# Exception to HTTP Response Mapping
# =============================================================================

def not_found_exception(resource: str, identifier: Any) -> HTTPException:
    """Create 404 HTTPException."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with id '{identifier}' not found",
    )


def forbidden_exception(message: str = "Permission denied") -> HTTPException:
    """Create 403 HTTPException."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message,
    )


def bad_request_exception(message: str) -> HTTPException:
    """Create 400 HTTPException."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


def conflict_exception(message: str) -> HTTPException:
    """Create 409 HTTPException."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message,
    )
