# Advanced Encapsulation Assignment

## 📌 Assignment Overview

**Advanced Practical Assignment — Encapsulation & Data Integrity in a Multi‑Module System**

This assignment focuses on implementing enterprise-grade encapsulation principles in a fintech context, demonstrating proper data hiding, state management, and composition patterns.

---

## 🎯 Scenario

You are part of a **fintech backend team** building a **user identity subsystem** for a digital banking application. 

### Context & Requirements

Because the system handles **sensitive information** (personal data, account relations, verification status), all classes must strictly follow:

- ✅ **Encapsulation** - Multi-level access control
- ✅ **Controlled Access** - Getter/setter methods with validation
- ✅ **Immutability** - Where needed for data integrity
- ✅ **State Transition Protection** - Prevent illegal state changes

### Your Mission

Design **three tightly-coupled classes**, each with increasing encapsulation rules, validation layers, and internal state management.

---

## 📋 Class Specifications

### 1️⃣ Class: `UserIdentity`

**Purpose**: Manage user identity information with strict encapsulation and validation.

#### Attributes

| Attribute | Access Level | Type | Validation | Description |
|-----------|-------------|------|------------|-------------|
| `username` | Public | `str` | None | User's display name |
| `_email` | Protected | `str` | ✅ Required | Validated email address |
| `__phone_number` | Private | `str` | ✅ Required | Validated phone (immutable) |
| `__verification_status` | Private | `str` | ✅ Enum | One of: `"UNVERIFIED"`, `"PENDING"`, `"VERIFIED"` |

#### Required Methods

##### Public Methods

```python
def get_email(self) -> str:
    """Return the protected email address."""
    
def set_email(self, new_email: str) -> None:
    """Set email after validation. Raises ValueError if invalid."""
    
def get_phone_number(self) -> str:
    """Return the private phone number."""
    
def get_verification_status(self) -> str:
    """Return current verification status."""
    
def request_verification(self) -> None:
    """
    Request verification (UNVERIFIED → PENDING).
    Raises ValueError if transition is illegal.
    """
    
def verify(self) -> None:
    """
    Complete verification (PENDING → VERIFIED).
    Raises ValueError if transition is illegal.
    """
```

##### Private Helper Methods (Required)

```python
def __validate_email(self, email: str) -> str:
    """Validate email format using regex. Raise ValueError if invalid."""
    
def __validate_phone(self, phone: str) -> str:
    """Validate phone format. Raise ValueError if invalid."""
    
def __log_state_change(self, message: str) -> None:
    """Log internal state changes with timestamp."""
```

#### Rules & Constraints

1. **State Machine Enforcement**:
   ```
   UNVERIFIED ──request_verification()──> PENDING ──verify()──> VERIFIED
   ```
   - Illegal transitions must be **blocked** with descriptive errors
   - Cannot skip states (e.g., UNVERIFIED → VERIFIED directly)
   - Cannot request verification if already PENDING or VERIFIED

2. **Validation**:
   - Email must match standard email regex pattern
   - Phone must follow international format (e.g., `+1-555-123-4567`)
   - Validation must occur in private helper methods

3. **Immutability**:
   - `__phone_number` is **immutable** after creation (no setter method)

4. **Logging**:
   - All state changes must be logged via `__log_state_change()`

---

### 2️⃣ Class: `AccountAccess`

**Purpose**: Manage user permissions with verification-based restrictions.

#### Attributes

| Attribute | Access Level | Type | Description |
|-----------|-------------|------|-------------|
| `__permissions` | Private | `list[str]` | List of granted permissions |

#### Class Constants

```python
RESTRICTED_PERMISSIONS = {"TRANSFER", "WITHDRAW"}
```

#### Required Methods

```python
def get_permissions(self) -> list[str]:
    """
    Return a COPY of permissions list.
    CRITICAL: Must return copy to prevent external modification.
    """
    
def add_permission(self, permission: str, is_verified: bool = True) -> None:
    """
    Add permission with verification check.
    
    Args:
        permission: Permission to add (e.g., "VIEW", "TRANSFER")
        is_verified: Whether user is verified
        
    Raises:
        ValueError: If restricted permission requires verification
    """
    
def remove_permission(self, permission: str) -> bool:
    """Remove permission. Return True if removed, False if not found."""
    
def has_permission(self, permission: str) -> bool:
    """Check if user has specific permission."""
```

#### Rules & Constraints

1. **Verification Restrictions**:
   - User who is **NOT VERIFIED** cannot receive:
     - `"TRANSFER"`
     - `"WITHDRAW"`
   - Attempting to grant these must raise `ValueError`

2. **Defensive Copying**:
   - `get_permissions()` **MUST** return a copy
   - Direct reference would allow external modification

3. **Case Handling**:
   - Permissions should be case-insensitive (convert to uppercase)

---

### 3️⃣ Class: `SecureUser` (Composition + Encapsulation)

**Purpose**: Unified facade combining identity and access control with comprehensive audit logging.

#### Attributes

| Attribute | Access Level | Type | Description |
|-----------|-------------|------|-------------|
| `_identity` | Protected | `UserIdentity` | User identity component |
| `__access` | Private | `AccountAccess` | Permission management component |
| `__audit_log` | Private | `list[dict]` | Audit trail of all actions |

#### Required Methods

```python
def grant_permission(self, permission: str) -> None:
    """
    Grant permission with verification enforcement.
    
    Must:
    1. Check if user is verified
    2. Call AccountAccess.add_permission()
    3. Log the action (success or failure)
    
    Raises:
        ValueError: If verification requirements not met
    """
    
def revoke_permission(self, permission: str) -> None:
    """
    Revoke permission and log the action.
    """
    
def identity_status(self) -> dict:
    """
    Return comprehensive identity information.
    
    Returns:
        {
            "username": str,
            "email": str,
            "phone": str,
            "verification_status": str,
            "permissions": list[str]
        }
    """
    
def get_audit_log(self) -> list[dict]:
    """
    Return COPY of audit log.
    
    Returns:
        List of audit entries with timestamp, action, details
    """
```

##### Additional Public Methods (Convenience)

```python
def request_verification(self) -> None:
    """Request verification and log action."""
    
def verify_identity(self) -> None:
    """Verify identity and log action."""
    
def update_email(self, new_email: str) -> None:
    """Update email and log action."""
```

##### Private Helper Methods (Required)

```python
def __log_action(self, action: str, details: str = "") -> None:
    """
    Log action to audit trail with timestamp.
    
    Format:
        {
            "timestamp": "YYYY-MM-DD HH:MM:SS",
            "action": "Action description",
            "details": "Additional context"
        }
    """
```

#### Rules & Constraints

1. **Composition**:
   - `SecureUser` **contains** (not inherits) `UserIdentity` and `AccountAccess`
   - Delegates operations to components
   - Provides unified interface

2. **Verification Enforcement**:
   - `grant_permission()` must check `_identity.get_verification_status()`
   - Pass verification status to `__access.add_permission()`

3. **Comprehensive Logging**:
   - **ALL** actions must be logged via `__log_action()`
   - Log both successes and failures
   - Include timestamps

4. **Defensive Copying**:
   - `get_audit_log()` must return a copy
   - Prevents external audit trail tampering

---

## 4️⃣ Demonstration: `main.py`

### Required Demonstrations

Your `main.py` must demonstrate **ALL** of the following scenarios:

#### ✅ 1. Valid Usage

```python
# Create user with valid data
user = SecureUser("john_doe", "john@example.com", "+1-555-123-4567")

# Grant basic permissions (works for unverified users)
user.grant_permission("VIEW")
user.grant_permission("EDIT")

# Complete verification workflow
user.request_verification()
user.verify_identity()

# Grant restricted permissions (now allowed)
user.grant_permission("TRANSFER")
user.grant_permission("WITHDRAW")
```

#### ❌ 2. Illegal Direct Access Attempts

```python
# These should FAIL with AttributeError (comment the expected errors)
# user.__access  # AttributeError: private attribute
# user.__audit_log  # AttributeError: private attribute
# user._identity.__phone_number  # AttributeError: name mangling
```

#### ❌ 3. Attempted Illegal State Transitions

```python
# Try to verify without requesting first
try:
    user.verify_identity()  # Should raise ValueError
except ValueError as e:
    print(f"Expected error: {e}")

# Try to request verification twice
user.request_verification()
try:
    user.request_verification()  # Should raise ValueError
except ValueError as e:
    print(f"Expected error: {e}")
```

#### ❌ 4. Granting Restricted Permissions Before Verification

```python
# Unverified user tries to get restricted permission
unverified_user = SecureUser("alice", "alice@test.com", "+1-555-999-8888")

try:
    unverified_user.grant_permission("TRANSFER")  # Should raise ValueError
except ValueError as e:
    print(f"Expected error: {e}")
```

#### ❌ 5. Attempting to Modify Returned Lists

```python
# Get permissions list and try to modify it
permissions = user.identity_status()['permissions']
permissions.append("FAKE_PERMISSION")  # Modifies only the copy!

# Verify internal state is unchanged
actual_permissions = user.identity_status()['permissions']
assert "FAKE_PERMISSION" not in actual_permissions
```

#### 📊 6. Final Formatted State Output

```python
# Display comprehensive user status
status = user.identity_status()
print(f"Username: {status['username']}")
print(f"Email: {status['email']}")
print(f"Phone: {status['phone']}")
print(f"Verification: {status['verification_status']}")
print(f"Permissions: {status['permissions']}")

# Display audit log
for entry in user.get_audit_log():
    print(f"[{entry['timestamp']}] {entry['action']}: {entry['details']}")
```

---

## 📦 Deliverables

### Required Files

1. ✅ **`user_identity.py`** - UserIdentity class implementation
2. ✅ **`account_access.py`** - AccountAccess class implementation  
3. ✅ **`secure_user.py`** - SecureUser class implementation
4. ✅ **`main.py`** - Comprehensive demonstration script

### Required Documentation

5. ✅ **Written Explanation** covering:

   **a) How encapsulation protects internal state**
   - Explanation of public/protected/private access levels
   - How name mangling prevents external access
   - Examples of state protection mechanisms

   **b) Why exposing lists is unsafe**
   - Security risks of returning direct references
   - How external code could bypass validation
   - Defensive copying solution

   **c) Why composition enhances system safety**
   - Separation of concerns
   - Enhanced encapsulation through delegation
   - Flexibility and maintainability benefits

---

## 🎯 Grading Criteria

### Functionality (40%)

- [ ] All classes implement required attributes with correct access levels
- [ ] All required methods are implemented
- [ ] Validation works correctly (email, phone)
- [ ] State transitions enforced properly
- [ ] Verification restrictions work
- [ ] Defensive copying implemented

### Encapsulation (30%)

- [ ] Public attributes used only where specified
- [ ] Protected attributes use single underscore
- [ ] Private attributes use double underscore
- [ ] Private helper methods are truly private
- [ ] No direct state manipulation possible
- [ ] Proper getter/setter usage

### Code Quality (20%)

- [ ] PEP 8 compliant
- [ ] Clear, descriptive variable names
- [ ] Comprehensive docstrings
- [ ] Proper error handling with descriptive messages
- [ ] No code duplication
- [ ] Clean, readable code structure

### Demonstration (10%)

- [ ] All required scenarios demonstrated
- [ ] Clear, formatted output
- [ ] Expected errors properly documented
- [ ] Comprehensive test coverage
- [ ] Final state output is complete

---

## 💡 Implementation Tips

### Email Validation Regex

```python
import re

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if not re.match(email_pattern, email):
    raise ValueError(f"Invalid email format: {email}")
```

### Phone Validation Example

```python
# Accept formats like: +1-555-123-4567, +44-20-1234-5678
# Must start with + and have appropriate length
if not phone.startswith("+") or len(phone.replace("-", "").replace(" ", "")) < 11:
    raise ValueError(f"Invalid phone format: {phone}")
```

### State Machine Pattern

```python
VALID_TRANSITIONS = {
    "UNVERIFIED": ["PENDING"],
    "PENDING": ["VERIFIED"],
    "VERIFIED": []
}

def can_transition_to(current_state, new_state):
    return new_state in VALID_TRANSITIONS.get(current_state, [])
```

### Defensive Copying

```python
# WRONG - Returns reference
def get_permissions(self):
    return self.__permissions  # External code can modify!

# CORRECT - Returns copy
def get_permissions(self):
    return self.__permissions.copy()  # Safe
```

### Audit Log Format

```python
from datetime import datetime

def __log_action(self, action, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.__audit_log.append({
        "timestamp": timestamp,
        "action": action,
        "details": details
    })
```

---

## ⚠️ Common Mistakes to Avoid

### ❌ DON'T:

1. **Skip validation**
   ```python
   self._email = email  # BAD! No validation
   ```

2. **Return direct references**
   ```python
   return self.__permissions  # BAD! Can be modified externally
   ```

3. **Allow invalid state transitions**
   ```python
   self.__verification_status = "VERIFIED"  # BAD! Skips PENDING
   ```

4. **Expose private methods**
   ```python
   def validate_email(self, email):  # BAD! Should be __validate_email
   ```

5. **Forget to log actions**
   ```python
   def grant_permission(self, permission):
       self.__access.add_permission(permission)
       # BAD! No logging
   ```

### ✅ DO:

1. **Validate all inputs**
2. **Use defensive copying**
3. **Enforce state transitions**
4. **Keep helper methods private**
5. **Log all significant actions**

---

## 🚀 Getting Started

### Step-by-Step Approach

1. **Start with `UserIdentity`**
   - Implement `__init__` with validation
   - Add getter/setter methods
   - Implement verification state machine
   - Add private helper methods

2. **Then `AccountAccess`**
   - Implement permission storage
   - Add CRUD methods
   - Implement verification checks
   - Use defensive copying

3. **Then `SecureUser`**
   - Compose UserIdentity and AccountAccess
   - Implement delegation methods
   - Add audit logging
   - Coordinate verification checks

4. **Finally `main.py`**
   - Demonstrate all scenarios
   - Test edge cases
   - Show error handling
   - Display comprehensive output

---

## 📚 Learning Objectives

By completing this assignment, you will:

1. ✅ Understand multi-level encapsulation (public/protected/private)
2. ✅ Master state machine implementation
3. ✅ Learn defensive programming techniques
4. ✅ Understand composition vs inheritance
5. ✅ Practice input validation
6. ✅ Implement audit logging
7. ✅ Handle errors gracefully
8. ✅ Write professional, maintainable code

---

## 🎓 Bonus Challenges (Optional)

For extra credit, implement:

1. **Password Management**
   - Add hashed password storage
   - Implement password change with old password verification

2. **Rate Limiting**
   - Limit verification requests (e.g., 3 per hour)

3. **Permission Expiration**
   - Add time-based permission expiration

4. **Enhanced Audit Log**
   - Add IP address tracking
   - Add user agent information

5. **Unit Tests**
   - Write comprehensive test suite
   - Test all edge cases

---

## ✅ Submission Checklist

Before submitting, verify:

- [ ] All 4 Python files are complete
- [ ] Code runs without errors
- [ ] All required scenarios are demonstrated
- [ ] Encapsulation rules are followed
- [ ] Validation works correctly
- [ ] State transitions are enforced
- [ ] Defensive copying is implemented
- [ ] Audit logging is comprehensive
- [ ] Code is PEP 8 compliant
- [ ] Docstrings are complete
- [ ] Written explanation is thorough
- [ ] Output is clear and formatted

---

## 📞 Support

If you have questions:
1. Review the implementation tips
2. Check common mistakes section
3. Refer to provided code examples
4. Ask instructor during office hours

---

## 👤 Assignment Author

**Otabek Sadiridinov**
- GitHub: [@otabekoff](https://github.com/otabekoff)
- Repository: [expert-memory](https://github.com/otabekoff/expert-memory)

---

**Good luck! This assignment demonstrates real-world fintech security patterns used in production systems.** 🏦🔒
