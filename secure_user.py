"""
SecureUser Module
Combines UserIdentity and AccountAccess with composition and comprehensive audit logging.
"""

from datetime import datetime
from user_identity import UserIdentity
from account_access import AccountAccess


class SecureUser:
    """
    Secure user class that combines identity and access control
    with comprehensive audit logging.
    """
    
    def __init__(self, username, email, phone_number):
        """
        Initialize SecureUser with identity and access components.
        
        Args:
            username (str): Username
            email (str): Email address
            phone_number (str): Phone number
        """
        self._identity = UserIdentity(username, email, phone_number)  # Protected
        self.__access = AccountAccess()  # Private
        self.__audit_log = []  # Private
        
        self.__log_action("SecureUser created", f"Username: {username}")
    
    def grant_permission(self, permission):
        """
        Grant permission with verification enforcement.
        
        Args:
            permission (str): Permission to grant
            
        Raises:
            ValueError: If verification requirements are not met
        """
        is_verified = self._identity.get_verification_status() == "VERIFIED"
        
        try:
            self.__access.add_permission(permission, is_verified)
            self.__log_action(
                "Permission granted",
                f"Permission: {permission}, Verified: {is_verified}"
            )
        except ValueError as e:
            self.__log_action(
                "Permission grant FAILED",
                f"Permission: {permission}, Reason: {str(e)}"
            )
            raise
    
    def revoke_permission(self, permission):
        """
        Revoke a permission from the user.
        
        Args:
            permission (str): Permission to revoke
        """
        removed = self.__access.remove_permission(permission)
        action = "revoked" if removed else "revoke failed (not found)"
        self.__log_action(f"Permission {action}", f"Permission: {permission}")
    
    def identity_status(self):
        """
        Get comprehensive identity status information.
        
        Returns:
            dict: Identity status information
        """
        return {
            "username": self._identity.username,
            "email": self._identity.get_email(),
            "phone": self._identity.get_phone_number(),
            "verification_status": self._identity.get_verification_status(),
            "permissions": self.__access.get_permissions()
        }
    
    def request_verification(self):
        """Request identity verification."""
        try:
            self._identity.request_verification()
            self.__log_action("Verification requested", "Status: PENDING")
        except ValueError as e:
            self.__log_action("Verification request FAILED", str(e))
            raise
    
    def verify_identity(self):
        """Verify the user's identity."""
        try:
            self._identity.verify()
            self.__log_action("Identity verified", "Status: VERIFIED")
        except ValueError as e:
            self.__log_action("Verification FAILED", str(e))
            raise
    
    def update_email(self, new_email):
        """
        Update user's email address.
        
        Args:
            new_email (str): New email address
        """
        old_email = self._identity.get_email()
        try:
            self._identity.set_email(new_email)
            self.__log_action("Email updated", f"{old_email} -> {new_email}")
        except ValueError as e:
            self.__log_action("Email update FAILED", str(e))
            raise
    
    def get_audit_log(self):
        """
        Return a COPY of the audit log to prevent external modification.
        
        Returns:
            list: Copy of audit log entries
        """
        return self.__audit_log.copy()
    
    def __log_action(self, action, details=""):
        """
        Private method to log all actions with timestamp.
        
        Args:
            action (str): Action performed
            details (str): Additional details
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "details": details
        }
        self.__audit_log.append(log_entry)
    
    def __str__(self):
        """String representation of SecureUser."""
        status = self.identity_status()
        return (f"SecureUser(username='{status['username']}', "
                f"status='{status['verification_status']}', "
                f"permissions={status['permissions']})")
