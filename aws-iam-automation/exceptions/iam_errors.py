class IAMManagerError(Exception):
    """Base exception for IAM management operations."""
    pass

class ResourceCreationError(IAMManagerError):
    """Raised when an IAM resource cannot be created."""
    # Ten błąd zostanie rzucony, gdy AWS API zwróci błąd podczas tworzenia zasobów
    pass