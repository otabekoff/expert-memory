# Advanced Encapsulation Assignment - Fintech Identity System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

A sophisticated Python implementation demonstrating advanced encapsulation principles, data integrity, and state management in a fintech user identity subsystem.

## 📝 Assignment Information

> **📋 For complete assignment details, requirements, and specifications, see [ASSIGNMENT.md](ASSIGNMENT.md)**

The [ASSIGNMENT.md](ASSIGNMENT.md) file contains:
- ✅ **Detailed task requirements** and specifications for all 3 classes
- ✅ **Complete API documentation** with method signatures and rules
- ✅ **Grading criteria** and evaluation guidelines
- ✅ **Implementation tips** (regex patterns, state machines, defensive copying)
- ✅ **Common mistakes** to avoid
- ✅ **Step-by-step approach** for building the system
- ✅ **Bonus challenges** for extra credit

This README provides an overview and usage guide, while ASSIGNMENT.md contains the full educational requirements.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Key Concepts](#key-concepts)
- [Examples](#examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a secure user identity and access control system for a digital banking application. It demonstrates enterprise-grade encapsulation patterns, including:

- **Multi-level access control** (public, protected, private attributes)
- **Defensive copying** to prevent state corruption
- **Composition over inheritance** for enhanced modularity
- **State machine implementation** for verification workflows
- **Comprehensive audit logging** for compliance
- **Input validation** for data integrity

## ✨ Features

### UserIdentity Class
- ✅ Validated email and phone number fields
- ✅ Controlled verification state transitions
- ✅ Immutable phone numbers after creation
- ✅ Private validation methods
- ✅ State change logging

### AccountAccess Class
- ✅ Private permissions management
- ✅ Defensive list copying
- ✅ Verification-based permission restrictions
- ✅ CRUD operations for permissions

### SecureUser Class (Composition)
- ✅ Unified interface for identity and access
- ✅ Coordinated permission granting with verification checks
- ✅ Comprehensive audit trail
- ✅ Defense-in-depth security architecture

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           SecureUser (Facade)           │
│  • Coordinates identity & access        │
│  • Enforces business rules              │
│  • Maintains audit log                  │
└────────────┬───────────────┬────────────┘
             │               │
    ┌────────▼──────┐   ┌───▼──────────┐
    │ UserIdentity  │   │ AccountAccess │
    │ • Email       │   │ • Permissions │
    │ • Phone       │   │ • Validation  │
    │ • Verification│   │ • Restrictions│
    └───────────────┘   └───────────────┘
```

### Design Patterns Used
- **Facade Pattern**: `SecureUser` provides unified interface
- **State Pattern**: Verification status state machine
- **Composition Pattern**: Component-based architecture
- **Template Method**: Validation pipelines

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- No external dependencies required (uses standard library only)

### Setup

```bash
# Clone or download the repository
cd d:\learn\py_assignments\19.11.2025

# Verify Python version
python --version

# Run the demonstration
python main.py
```

## 💻 Usage

### Basic Example

```python
from secure_user import SecureUser

# Create a secure user
user = SecureUser(
    username="john_doe",
    email="john@example.com",
    phone_number="+1-555-123-4567"
)

# Grant basic permissions (works for unverified users)
user.grant_permission("VIEW")
user.grant_permission("EDIT")

# Request and complete verification
user.request_verification()
user.verify_identity()

# Grant restricted permissions (requires verification)
user.grant_permission("TRANSFER")
user.grant_permission("WITHDRAW")

# Check status
status = user.identity_status()
print(f"User: {status['username']}")
print(f"Verified: {status['verification_status']}")
print(f"Permissions: {status['permissions']}")

# Review audit log
for entry in user.get_audit_log():
    print(f"[{entry['timestamp']}] {entry['action']}")
```

### Verification Workflow

```python
# State transition flow
user = SecureUser("alice", "alice@bank.com", "+1-555-999-8888")

# Initial state: UNVERIFIED
print(user.identity_status()['verification_status'])  # UNVERIFIED

# Request verification
user.request_verification()
print(user.identity_status()['verification_status'])  # PENDING

# Complete verification
user.verify_identity()
print(user.identity_status()['verification_status'])  # VERIFIED
```

### Error Handling

```python
from secure_user import SecureUser

try:
    # Attempt to grant restricted permission without verification
    user = SecureUser("bob", "bob@test.com", "+1-555-111-2222")
    user.grant_permission("TRANSFER")  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid state transition
    user.verify_identity()  # Must request first
except ValueError as e:
    print(f"Error: {e}")
```

## 📁 Project Structure

```
19.11.2025/
│
├── user_identity.py          # UserIdentity class (identity management)
├── account_access.py         # AccountAccess class (permission management)
├── secure_user.py            # SecureUser class (composition facade)
├── main.py                   # Comprehensive demonstration
│
├── README.md                 # This file
├── EXPLANATION.md            # Detailed technical explanation
├── CONTRIBUTING.md           # Contribution guidelines
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT License
├── SECURITY.md               # Security policy
└── CODE_OF_CONDUCT.md        # Community guidelines
```

## 🔑 Key Concepts

### 1. Encapsulation Levels

| Level | Syntax | Access | Use Case |
|-------|--------|--------|----------|
| Public | `attribute` | External & internal | Non-sensitive data |
| Protected | `_attribute` | Internal & subclasses | Intended for internal use |
| Private | `__attribute` | Internal only (name mangled) | Sensitive data, state |

### 2. Defensive Copying

```python
# UNSAFE - returns reference
def get_permissions(self):
    return self.__permissions  # External code can modify!

# SAFE - returns copy
def get_permissions(self):
    return self.__permissions.copy()  # External modifications isolated
```

### 3. State Machine

```
UNVERIFIED ──request_verification()──> PENDING ──verify()──> VERIFIED
     ↑                                     ↑                      ↑
     └─────────── (illegal transitions blocked) ─────────────────┘
```

### 4. Validation Pipeline

```python
Input → Validation → Sanitization → Storage → Logging
```

## 📚 Examples

### Example 1: Complete User Lifecycle

```python
from secure_user import SecureUser

# 1. User creation with validation
user = SecureUser("john_doe", "john@bank.com", "+1-555-123-4567")

# 2. Grant initial permissions
user.grant_permission("VIEW")
user.grant_permission("EDIT")

# 3. Verification workflow
user.request_verification()
user.verify_identity()

# 4. Grant advanced permissions
user.grant_permission("TRANSFER")
user.grant_permission("WITHDRAW")

# 5. Update email
user.update_email("john.new@bank.com")

# 6. Revoke permission
user.revoke_permission("EDIT")

# 7. Review audit trail
audit_log = user.get_audit_log()
print(f"Total actions: {len(audit_log)}")
```

### Example 2: Validation Demonstrations

```python
# Valid phone formats
valid_phones = [
    "+1-555-123-4567",
    "+44-20-1234-5678",
    "+86-10-1234-5678"
]

# Invalid phone formats (will raise ValueError)
invalid_phones = [
    "123-4567",           # Too short
    "not-a-phone",        # Invalid format
    "5551234567"          # Missing country code
]

# Valid email formats
valid_emails = [
    "user@example.com",
    "john.doe@company.co.uk",
    "test_user+tag@domain.com"
]

# Invalid email formats (will raise ValueError)
invalid_emails = [
    "notanemail",
    "@example.com",
    "user@",
    "user@.com"
]
```

## 🧪 Testing

Run the comprehensive demonstration:

```bash
python main.py
```

The demonstration includes:
1. Valid user creation
2. Illegal direct access attempts
3. Basic permission granting
4. Restricted permission enforcement
5. Illegal state transitions
6. Proper verification workflow
7. Email validation
8. Permission revocation
9. Phone number immutability
10. Comprehensive audit logging
11. Invalid user creation attempts

## 📖 Further Reading

- [EXPLANATION.md](EXPLANATION.md) - Detailed technical explanation
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [SECURITY.md](SECURITY.md) - Security policy
- [CHANGELOG.md](CHANGELOG.md) - Version history

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

- **Otabek Sadiridinov** ([@otabekoff](https://github.com/otabekoff)) - Advanced Python Encapsulation Assignment

## 🙏 Acknowledgments

- Python Software Foundation for excellent documentation
- Fintech security best practices from OWASP
- Design patterns from Gang of Four
- PEP 8 style guide

## 📞 Support

For questions or issues:
1. Check the [EXPLANATION.md](EXPLANATION.md) for detailed concepts
2. Review the [main.py](main.py) demonstration
3. Open an issue for bugs or feature requests

## 🔄 Version

Current version: 1.0.0 (See [CHANGELOG.md](CHANGELOG.md) for details)

---

**Note**: This is an educational project demonstrating advanced encapsulation principles in Python. For production fintech applications, additional security measures, database integration, and regulatory compliance features would be required.
