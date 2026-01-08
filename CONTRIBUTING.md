# Contributing to PQC Migration Risk Model

Thank you for your interest in contributing to the PQC Migration Risk Model framework. This document provides guidelines for contributing to the project.

## How to Report Issues

If you find a bug or have a suggestion for improvement:

1. Check the existing issues to see if it has already been reported
2. If not, create a new issue with a clear title and description
3. Include relevant details such as:
   - Steps to reproduce the problem
   - Expected behavior vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Any error messages or logs

## Code Contribution Process

### Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. Write clear, concise code that follows the project's style guidelines
2. Add tests for any new functionality
3. Update documentation as needed
4. Ensure all tests pass before submitting

### Submitting Changes

1. Commit your changes with clear, descriptive commit messages
2. Push your branch to your fork
3. Submit a pull request to the main repository
4. Provide a clear description of the changes and their purpose
5. Reference any related issues

## Code Style Guidelines

This project follows PEP 8 style guidelines for Python code:

- Use 4 spaces for indentation (no tabs)
- Maximum line length of 88 characters (compatible with Black formatter)
- Use descriptive variable and function names
- Add docstrings to all functions, classes, and modules
- Keep functions focused and single-purpose

### Example Docstring Format

```python
def calculate_metric(value, threshold):
    """
    Calculate a normalized metric based on value and threshold.
    
    Args:
        value (float): The raw metric value
        threshold (float): The threshold for normalization
        
    Returns:
        float: Normalized metric in range [0, 1]
    """
    return min(1.0, value / threshold)
```

## Testing Requirements

- All new features must include unit tests
- Tests should be placed in the `tests/` directory
- Use pytest for testing
- Aim for high test coverage of new code
- Run tests locally before submitting:
  ```bash
  pytest tests/
  ```

## Documentation Standards

- Update the README.md if your changes affect usage or setup
- Add docstrings to all new functions and classes
- Include equation references from the paper where applicable
- Keep comments concise and meaningful
- Update example scripts if they are affected by your changes

## Development Workflow

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8
   ```

2. Make your changes following the guidelines above

3. Run tests:
   ```bash
   pytest tests/
   ```

4. Format code (optional but recommended):
   ```bash
   black *.py examples/*.py tests/*.py
   ```

5. Check style (optional):
   ```bash
   flake8 *.py examples/*.py tests/*.py
   ```

## Questions or Need Help?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact the maintainers listed in the README
- Review existing pull requests for examples

Thank you for contributing to the advancement of post-quantum cryptography research!
