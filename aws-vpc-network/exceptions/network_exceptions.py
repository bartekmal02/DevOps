class NetworkError(Exception):
    """Base exception for network-related errors."""
    pass

class VpcCreationError(NetworkError):
    """Raised when VPC creation fails."""
    pass

class SubnetCreationError(NetworkError):
    """Raised when Subnet creation fails."""
    pass