"""
Main Demonstration Module
Demonstrates encapsulation, validation, state transitions, and security features.
"""

from secure_user import SecureUser


def print_section(title):
    """Helper function to print formatted section headers."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_status(user):
    """Helper function to print user status in formatted way."""
    status = user.identity_status()
    print(f"\nCurrent Status:")
    print(f"  Username: {status['username']}")
    print(f"  Email: {status['email']}")
    print(f"  Phone: {status['phone']}")
    print(f"  Verification: {status['verification_status']}")
    print(f"  Permissions: {status['permissions']}")


def print_audit_log(user):
    """Helper function to print audit log."""
    print("\nAudit Log:")
    for entry in user.get_audit_log():
        print(f"  [{entry['timestamp']}] {entry['action']}")
        if entry['details']:
            print(f"    └─ {entry['details']}")


def main():
    print_section("1. CREATING SECURE USER WITH VALID DATA")
    
    # Create a secure user with valid data
    user = SecureUser(
        username="john_doe",
        email="john.doe@example.com",
        phone_number="+1-555-123-4567"
    )
    print_status(user)
    
    
    print_section("2. ATTEMPTING ILLEGAL DIRECT ACCESS (WILL FAIL)")
    
    print("\n# Trying to access private attributes directly:")
    print("# user.__access  # AttributeError: private attribute")
    print("# user.__audit_log  # AttributeError: private attribute")
    
    try:
        # This will fail due to name mangling
        print(user.__access)
    except AttributeError as e:
        print(f"✓ Expected error: {e}")
    
    try:
        # This will also fail
        print(user.__audit_log)
    except AttributeError as e:
        print(f"✓ Expected error: {e}")
    
    print("\n# Trying to modify returned permissions list:")
    permissions = user.identity_status()['permissions']
    permissions.append("FAKE_PERMISSION")
    print(f"Modified external list: {permissions}")
    print(f"Actual user permissions: {user.identity_status()['permissions']}")
    print("✓ Internal state remains protected due to copy!")
    
    
    print_section("3. GRANTING BASIC PERMISSIONS (UNVERIFIED USER)")
    
    # Grant basic permissions - these should work
    try:
        user.grant_permission("VIEW")
        print("✓ Successfully granted VIEW permission")
    except ValueError as e:
        print(f"✗ Failed: {e}")
    
    try:
        user.grant_permission("EDIT")
        print("✓ Successfully granted EDIT permission")
    except ValueError as e:
        print(f"✗ Failed: {e}")
    
    print_status(user)
    
    
    print_section("4. ATTEMPTING RESTRICTED PERMISSIONS (UNVERIFIED USER)")
    
    # Try to grant restricted permissions - should fail
    print("\nTrying to grant TRANSFER permission without verification:")
    try:
        user.grant_permission("TRANSFER")
        print("✗ This should not succeed!")
    except ValueError as e:
        print(f"✓ Expected failure: {e}")
    
    print("\nTrying to grant WITHDRAW permission without verification:")
    try:
        user.grant_permission("WITHDRAW")
        print("✗ This should not succeed!")
    except ValueError as e:
        print(f"✓ Expected failure: {e}")
    
    print_status(user)
    
    
    print_section("5. ILLEGAL STATE TRANSITIONS")
    
    print("\nAttempting to verify without requesting first:")
    try:
        user.verify_identity()
        print("✗ This should not succeed!")
    except ValueError as e:
        print(f"✓ Expected failure: {e}")
    
    
    print_section("6. PROPER VERIFICATION WORKFLOW")
    
    print("\nRequesting verification...")
    user.request_verification()
    print_status(user)
    
    print("\nAttempting to request verification again (should fail):")
    try:
        user.request_verification()
        print("✗ This should not succeed!")
    except ValueError as e:
        print(f"✓ Expected failure: {e}")
    
    print("\nVerifying user identity...")
    user.verify_identity()
    print_status(user)
    
    
    print_section("7. GRANTING RESTRICTED PERMISSIONS (VERIFIED USER)")
    
    print("\nNow that user is verified, granting restricted permissions:")
    try:
        user.grant_permission("TRANSFER")
        print("✓ Successfully granted TRANSFER permission")
    except ValueError as e:
        print(f"✗ Failed: {e}")
    
    try:
        user.grant_permission("WITHDRAW")
        print("✓ Successfully granted WITHDRAW permission")
    except ValueError as e:
        print(f"✗ Failed: {e}")
    
    print_status(user)
    
    
    print_section("8. EMAIL UPDATE WITH VALIDATION")
    
    print("\nUpdating email to valid address:")
    try:
        user.update_email("john.newemail@company.com")
        print("✓ Email updated successfully")
    except ValueError as e:
        print(f"✗ Failed: {e}")
    
    print("\nAttempting to update with invalid email:")
    try:
        user.update_email("invalid-email-format")
        print("✗ This should not succeed!")
    except ValueError as e:
        print(f"✓ Expected failure: {e}")
    
    print_status(user)
    
    
    print_section("9. PERMISSION REVOCATION")
    
    print("\nRevoking EDIT permission:")
    user.revoke_permission("EDIT")
    print_status(user)
    
    
    print_section("10. TESTING IMMUTABILITY OF PHONE NUMBER")
    
    print("\nPhone number is immutable after creation.")
    print("There is no set_phone_number() method - only get_phone_number()")
    print(f"Current phone: {user.identity_status()['phone']}")
    
    
    print_section("11. COMPREHENSIVE AUDIT LOG")
    
    print_audit_log(user)
    
    
    print_section("12. FINAL STATE SUMMARY")
    
    print_status(user)
    print(f"\nTotal audit log entries: {len(user.get_audit_log())}")
    
    
    print_section("13. DEMONSTRATION OF INVALID USER CREATION")
    
    print("\nTrying to create user with invalid email:")
    try:
        invalid_user = SecureUser(
            username="jane_doe",
            email="invalid.email",
            phone_number="+1-555-999-8888"
        )
        print("✗ This should not succeed!")
    except ValueError as e:
        print(f"✓ Expected failure: {e}")
    
    print("\nTrying to create user with invalid phone:")
    try:
        invalid_user = SecureUser(
            username="jane_doe",
            email="jane@example.com",
            phone_number="123-456"
        )
        print("✗ This should not succeed!")
    except ValueError as e:
        print(f"✓ Expected failure: {e}")
    
    
    print("\n" + "=" * 70)
    print(" DEMONSTRATION COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
