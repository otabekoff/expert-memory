"""
AccountAccess Module
Manages user permissions with strict encapsulation and verification requirements.
"""


class AccountAccess:
    """
    Manages user permissions with private permissions list.
    Enforces verification requirements for sensitive operations.
    """
    
    # Class-level constants for restricted permissions
    RESTRICTED_PERMISSIONS = {"TRANSFER", "WITHDRAW"}
    
    def __init__(self):
        """Initialize AccountAccess with empty permissions list."""
        self.__permissions = []  # Private attribute
    
    def get_permissions(self):
        """
        Return a COPY of the permissions list to prevent external modification.
        
        Returns:
            list: Copy of permissions
        """
        return self.__permissions.copy()
    
    def add_permission(self, permission, is_verified=True):
        """
        Add a permission to the user's access list.
        
        Args:
            permission (str): Permission to add
            is_verified (bool): Whether the user is verified
            
        Raises:
            ValueError: If trying to add restricted permission without verification
        """
        permission = permission.upper()
        
        # Check if permission is restricted and user is not verified
        if permission in self.RESTRICTED_PERMISSIONS and not is_verified:
            raise ValueError(
                f"Cannot grant '{permission}' permission. "
                f"User must be VERIFIED to receive restricted permissions."
            )
        
        # Add permission if not already present
        if permission not in self.__permissions:
            self.__permissions.append(permission)
        else:
            print(f"Permission '{permission}' already exists.")
    
    def remove_permission(self, permission):
        """
        Remove a permission from the user's access list.
        
        Args:
            permission (str): Permission to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        permission = permission.upper()
        
        if permission in self.__permissions:
            self.__permissions.remove(permission)
            return True
        else:
            print(f"Permission '{permission}' not found.")
            return False
    
    def has_permission(self, permission):
        """
        Check if user has a specific permission.
        
        Args:
            permission (str): Permission to check
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        return permission.upper() in self.__permissions
    
    def __str__(self):
        """String representation of AccountAccess."""
        return f"AccountAccess(permissions={self.__permissions})"
