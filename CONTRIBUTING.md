# Contributing to Advanced Encapsulation Assignment

First off, thank you for considering contributing to this project! It's people like you that make this educational resource valuable for learning advanced Python encapsulation concepts.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Testing Guidelines](#testing-guidelines)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear, descriptive title**
- **Exact steps to reproduce the problem**
- **Expected behavior**
- **Actual behavior**
- **Python version** (`python --version`)
- **Operating system**
- **Code sample** demonstrating the issue

Example bug report:

```markdown
## Bug: Email validation accepts invalid format

**Steps to reproduce:**
1. Create UserIdentity with email "user@"
2. No exception is raised

**Expected:** ValueError should be raised
**Actual:** Email is accepted
**Python Version:** 3.9.5
**OS:** Windows 10
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear, descriptive title**
- **Detailed description** of the proposed enhancement
- **Use cases** that would benefit from this enhancement
- **Example code** showing how it would be used
- **Potential implementation** approach (optional)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes** following the coding standards
4. **Test thoroughly**
5. **Commit your changes** using conventional commits
6. **Push to your fork** (`git push origin feature/AmazingFeature`)
7. **Open a Pull Request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Text editor or IDE (VS Code recommended)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/py_assignments.git
cd py_assignments/19.11.2025

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run the demonstration to verify setup
python main.py
```

### Project Structure Understanding

```
19.11.2025/
│
├── user_identity.py          # Identity management with validation
├── account_access.py         # Permission management
├── secure_user.py            # Composition facade
├── main.py                   # Demonstration & testing
│
└── docs/                     # Documentation files
    ├── README.md
    ├── EXPLANATION.md
    └── ...
```

## 📏 Coding Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specifics:

#### Naming Conventions

```python
# Classes: PascalCase
class UserIdentity:
    pass

# Functions/Methods: snake_case
def validate_email(email):
    pass

# Constants: UPPER_SNAKE_CASE
RESTRICTED_PERMISSIONS = {"TRANSFER", "WITHDRAW"}

# Private methods: __double_underscore
def __validate_phone(self, phone):
    pass

# Protected attributes: _single_underscore
self._email = email

# Private attributes: __double_underscore
self.__verification_status = "UNVERIFIED"
```

#### Docstrings

Use Google-style docstrings for all public methods:

```python
def grant_permission(self, permission):
    """
    Grant a permission to the user with verification enforcement.
    
    Args:
        permission (str): Permission to grant (e.g., "VIEW", "TRANSFER")
        
    Raises:
        ValueError: If permission is restricted and user is not verified
        
    Example:
        >>> user.grant_permission("VIEW")
        >>> user.grant_permission("TRANSFER")  # Requires verification
    """
    pass
```

#### Code Organization

```python
# 1. Module docstring
"""
Module description here.
"""

# 2. Imports (standard library first, then third-party, then local)
import re
from datetime import datetime

# 3. Constants
RESTRICTED_PERMISSIONS = {"TRANSFER", "WITHDRAW"}

# 4. Classes
class MyClass:
    """Class docstring."""
    
    # 4a. Class variables
    class_var = "value"
    
    # 4b. __init__
    def __init__(self):
        pass
    
    # 4c. Public methods
    def public_method(self):
        pass
    
    # 4d. Protected methods
    def _protected_method(self):
        pass
    
    # 4e. Private methods
    def __private_method(self):
        pass
    
    # 4f. Special methods (__str__, __repr__)
    def __str__(self):
        pass
```

### Encapsulation Requirements

When contributing code, maintain strict encapsulation:

#### ✅ DO:
```python
# Use private attributes for sensitive data
self.__verification_status = "UNVERIFIED"

# Return copies of mutable objects
def get_permissions(self):
    return self.__permissions.copy()

# Validate all inputs
def set_email(self, email):
    validated = self.__validate_email(email)
    self._email = validated

# Use getters/setters for controlled access
def get_verification_status(self):
    return self.__verification_status
```

#### ❌ DON'T:
```python
# Don't expose mutable references
def get_permissions(self):
    return self.__permissions  # BAD!

# Don't skip validation
def set_email(self, email):
    self._email = email  # BAD! No validation

# Don't allow direct attribute access for sensitive data
self.verification_status = "VERIFIED"  # BAD! Should be private
```

## 📝 Commit Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/):

### Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring (no feature change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Feature addition
git commit -m "feat(UserIdentity): add password reset functionality"

# Bug fix
git commit -m "fix(AccountAccess): prevent duplicate permissions"

# Documentation
git commit -m "docs(README): add installation instructions"

# Refactoring
git commit -m "refactor(SecureUser): extract validation logic"
```

## 🔄 Pull Request Process

### Before Submitting

1. ✅ **Test your changes** thoroughly
2. ✅ **Update documentation** if needed
3. ✅ **Follow coding standards**
4. ✅ **Write clear commit messages**
5. ✅ **Update CHANGELOG.md** with your changes

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe how you tested your changes:
- Test scenario 1
- Test scenario 2

## Checklist
- [ ] Code follows PEP 8 style guide
- [ ] All methods have docstrings
- [ ] Changes are thoroughly tested
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

### Review Process

1. Maintainer will review within 3-5 days
2. Address any requested changes
3. Once approved, maintainer will merge
4. Your contribution will be acknowledged in CHANGELOG.md

## 🎨 Style Guide

### Code Formatting

```python
# Line length: Maximum 88 characters (Black formatter style)
# Indentation: 4 spaces (no tabs)

# Good
def long_function_name(
    parameter_one, parameter_two, parameter_three,
    parameter_four, parameter_five
):
    pass

# Imports: Grouped and sorted
import os
import sys

from datetime import datetime
from typing import List, Optional

from user_identity import UserIdentity
```

### Comments

```python
# Use comments to explain WHY, not WHAT
def verify(self):
    # Check PENDING state to prevent unauthorized verification
    if self.__verification_status == "PENDING":
        self.__verification_status = "VERIFIED"
```

### Error Messages

```python
# Clear, actionable error messages
raise ValueError(
    f"Cannot grant '{permission}' permission. "
    f"User must be VERIFIED to receive restricted permissions."
)
```

## 🧪 Testing Guidelines

### Manual Testing

Always run `main.py` to verify your changes don't break existing functionality:

```bash
python main.py
```

### Test Cases to Verify

1. **Valid operations** complete successfully
2. **Invalid inputs** raise appropriate exceptions
3. **State transitions** follow rules
4. **Encapsulation** is maintained (no direct access)
5. **Defensive copying** works correctly

### Adding Test Scenarios

When adding new features, add demonstration code to `main.py`:

```python
def test_new_feature():
    print_section("NEW FEATURE TEST")
    
    user = SecureUser("test", "test@example.com", "+1-555-000-0000")
    
    # Test valid usage
    try:
        # Your test code here
        print("✓ Feature works correctly")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test invalid usage
    try:
        # Your test code that should fail
        print("✗ This should have failed!")
    except ValueError as e:
        print(f"✓ Expected error: {e}")
```

## 🐛 Bug Triage

### Priority Levels

- **P0 - Critical**: System crashes, data corruption
- **P1 - High**: Major feature broken, security issue
- **P2 - Medium**: Minor feature broken, poor UX
- **P3 - Low**: Cosmetic, documentation typo

## 💡 Feature Requests

### Good Feature Request Template

```markdown
## Feature: Two-Factor Authentication

**Problem:** Current system only verifies email/phone.

**Proposed Solution:** Add OTP verification step.

**Use Cases:**
- Enhanced security for financial transactions
- Compliance with banking regulations

**Example Usage:**
```python
user.request_verification()
user.send_otp()
user.verify_with_otp("123456")
```

**Implementation Considerations:**
- Need OTP generation/validation
- Time-based expiration
- Rate limiting
```

## 📚 Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Python Encapsulation](https://realpython.com/python-classes/)

## ❓ Questions?

If you have questions:
1. Check existing documentation
2. Review closed issues for similar questions
3. Open a new issue with the `question` label

## 🎉 Recognition

Contributors will be acknowledged in:
- CHANGELOG.md for each release
- README.md contributors section

## 👤 Project Author

**Otabek Sadiridinov**
- GitHub: [@otabekoff](https://github.com/otabekoff)
- Repository: [expert-memory](https://github.com/otabekoff/expert-memory)

Thank you for contributing to this educational project!
