"""
UserIdentity Module
Handles user identity information with strict encapsulation and validation.
"""

import re
from datetime import datetime


class UserIdentity:
    """
    Manages user identity with protected email, private phone number,
    and controlled verification status transitions.
    """
    
    def __init__(self, username, email, phone_number):
        """
        Initialize UserIdentity with validation.
        
        Args:
            username (str): Public username
            email (str): Email address (will be validated)
            phone_number (str): Phone number (will be validated)
        """
        self.username = username  # Public attribute
        self._email = None  # Protected attribute
        self.__phone_number = None  # Private attribute
        self.__verification_status = "UNVERIFIED"  # Private attribute
        
        # Validate and set email and phone during initialization
        self.set_email(email)
        self.__phone_number = self.__validate_phone(phone_number)
    
    # Email getter and setter
    def get_email(self):
        """Return the protected email address."""
        return self._email
    
    def set_email(self, new_email):
        """
        Set email after validation.
        
        Args:
            new_email (str): New email address
            
        Raises:
            ValueError: If email format is invalid
        """
        validated_email = self.__validate_email(new_email)
        old_email = self._email
        self._email = validated_email
        
        if old_email is not None:
            self.__log_state_change(f"Email changed from {old_email} to {validated_email}")
    
    # Phone number getter (no setter - immutable after creation)
    def get_phone_number(self):
        """Return the private phone number."""
        return self.__phone_number
    
    # Verification status management
    def get_verification_status(self):
        """Return the current verification status."""
        return self.__verification_status
    
    def request_verification(self):
        """
        Request verification. Only allowed from UNVERIFIED state.
        
        Raises:
            ValueError: If current state doesn't allow this transition
        """
        if self.__verification_status == "UNVERIFIED":
            self.__verification_status = "PENDING"
            self.__log_state_change("Verification requested: UNVERIFIED -> PENDING")
        elif self.__verification_status == "PENDING":
            raise ValueError("Verification already pending. Cannot request again.")
        elif self.__verification_status == "VERIFIED":
            raise ValueError("User already verified. Cannot request verification.")
    
    def verify(self):
        """
        Verify the user. Only allowed from PENDING state.
        
        Raises:
            ValueError: If current state doesn't allow this transition
        """
        if self.__verification_status == "PENDING":
            self.__verification_status = "VERIFIED"
            self.__log_state_change("User verified: PENDING -> VERIFIED")
        elif self.__verification_status == "UNVERIFIED":
            raise ValueError("Cannot verify. User must request verification first.")
        elif self.__verification_status == "VERIFIED":
            raise ValueError("User already verified.")
    
    # Private helper methods
    def __validate_email(self, email):
        """
        Validate email format using regex.
        
        Args:
            email (str): Email to validate
            
        Returns:
            str: Validated email
            
        Raises:
            ValueError: If email format is invalid
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError(f"Invalid email format: {email}")
        return email
    
    def __validate_phone(self, phone):
        """
        Validate phone number format (expects format: +X-XXX-XXX-XXXX or similar).
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            str: Validated phone number
            
        Raises:
            ValueError: If phone format is invalid
        """
        # Remove spaces and dashes for validation
        cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # Check if it starts with + and has 10-15 digits
        if phone.startswith("+") and len(cleaned) >= 11 and len(cleaned) <= 16:
            if cleaned[1:].isdigit():
                return phone
        
        raise ValueError(f"Invalid phone format: {phone}. Expected format: +X-XXX-XXX-XXXX")
    
    def __log_state_change(self, message):
        """
        Log internal state changes with timestamp.
        
        Args:
            message (str): Log message
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] UserIdentity LOG: {message}")
    
    def __str__(self):
        """String representation of UserIdentity."""
        return (f"UserIdentity(username='{self.username}', "
                f"email='{self._email}', "
                f"phone='{self.__phone_number}', "
                f"status='{self.__verification_status}')")
