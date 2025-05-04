# Contributing to SubscriptionSage

Thank you for your interest in contributing to SubscriptionSage! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Questions and Discussions](#questions-and-discussions)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/SubscriptionSage.git
   cd SubscriptionSage
   ```
3. Set up the development environment using Dev Containers (see [Development Guide](DEVELOPMENT.md))
4. Create a new branch for your feature or bugfix

## Development Workflow

1. **Create a Branch**
   - Branch naming convention:
     - Features: `feature/description`
     - Bug fixes: `fix/description`
     - Documentation: `docs/description`
     - Hotfixes: `hotfix/description`

2. **Make Changes**
   - Follow the [Style Guide](STYLE_GUIDE.md)
   - Write clear, descriptive commit messages
   - Keep changes focused and atomic
   - Update documentation as needed

3. **Test Your Changes**
   - Write or update tests as needed
   - Ensure all tests pass
   - Test your changes manually

4. **Submit a Pull Request**
   - Push your branch to your fork
   - Create a pull request against the main repository
   - Fill out the pull request template

## Pull Request Process

1. **Before Submitting**
   - Ensure your code follows the style guide
   - Update documentation for any new features
   - Add tests for new functionality
   - Ensure all tests pass
   - Update the changelog if applicable

2. **Pull Request Template**
   - Description of changes
   - Related issue number (if applicable)
   - Type of change (feature, bugfix, documentation)
   - Testing performed
   - Screenshots (if applicable)

3. **Review Process**
   - All pull requests require at least one review
   - Address any feedback from reviewers
   - Keep the pull request up to date with the main branch

## Development Guidelines

### Code Style

- Follow the [Style Guide](STYLE_GUIDE.md)
- Use meaningful variable and function names
- Write clear, concise comments
- Keep functions small and focused
- Use type hints for Python code

### Database Changes

- Create migrations for any database schema changes
- Test migrations both up and down
- Include data migration scripts if needed
- Document any breaking changes

### Frontend Development

- Follow BEM naming convention for CSS
- Use semantic HTML
- Ensure responsive design
- Test across different browsers
- Optimize assets

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_file.py

# Run with coverage
pytest --cov=.
```

### Writing Tests

- Write tests for new features
- Update tests for bug fixes
- Follow the AAA pattern (Arrange, Act, Assert)
- Use meaningful test names
- Test edge cases and error conditions

## Documentation

### Code Documentation

- Document all public APIs
- Use clear, concise docstrings
- Include examples for complex functions
- Keep documentation up to date

### User Documentation

- Update README.md for significant changes
- Document new features
- Update API documentation
- Include usage examples

## Questions and Discussions

- Use GitHub Issues for bug reports and feature requests
- Use GitHub Discussions for general questions
- Join our community chat (if available)
- Check existing issues and discussions before creating new ones

## Additional Resources

- [Development Guide](DEVELOPMENT.md)
- [Style Guide](STYLE_GUIDE.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Project Roadmap](ROADMAP.md) (if available)

## Getting Help

If you need help or have questions:

1. Check the documentation
2. Search existing issues and discussions
3. Create a new issue or discussion
4. Contact the maintainers at lukasz.korbasiewicz@gmail.com

Thank you for contributing to SubscriptionSage! 