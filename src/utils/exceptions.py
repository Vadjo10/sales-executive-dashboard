from __future__ import annotations


class SalesDashboardError(Exception):
    """Base exception for the project."""


class APIConnectionError(SalesDashboardError):
    """Failed to connect to the API."""


class APIRequestError(SalesDashboardError):
    """API returned an error response."""


class DataValidationError(SalesDashboardError):
    """Data failed validation checks."""


class DatabaseConnectionError(SalesDashboardError):
    """Failed to connect to the database."""


class DatabaseOperationError(SalesDashboardError):
    """Database operation failed."""


class CircuitBreakerOpenError(SalesDashboardError):
    """Circuit breaker is open, request blocked."""


class DataRejectedError(SalesDashboardError):
    """Data record failed validation and was rejected."""


class PipelineError(SalesDashboardError):
    """Pipeline execution failed."""
