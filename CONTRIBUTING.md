# Contributing to MCP Space Life Sciences KGs

Thank you for your interest in contributing! This project integrates GeneLab, PrimeKG, and SPOKE-OKN knowledge graphs to advance space life sciences research.

## How to Contribute

### Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include clear descriptions and steps to reproduce
- Specify your environment (Python version, OS, etc.)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Add tests** if applicable
5. **Run tests**: `pytest tests/`
6. **Check code style**: `black src/` and `flake8 src/`
7. **Commit changes**: Use clear, descriptive commit messages
8. **Push to your fork**: `git push origin feature/your-feature-name`
9. **Submit a Pull Request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/MCP_Space_Life_Science_KGs.git
cd MCP_Space_Life_Science_KGs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black src/
flake8 src/
```

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 100)
- Add docstrings to all functions and classes
- Include type hints where appropriate

### Testing

- Write tests for new features
- Maintain test coverage above 80%
- Test both unit and integration scenarios
- Include examples in docstrings

### Documentation

- Update README.md if adding new features
- Add docstrings to all new code
- Update relevant documentation files in `docs/`
- Include examples for new functionality

### Knowledge Graph Integration

When adding new queries or tools:

1. **For GeneLab/PrimeKG (Cypher)**:
   - Add queries to `src/mcp_space_life_sciences/cypher_queries.py`
   - Follow existing query template patterns
   - Include parameter documentation

2. **For SPOKE-OKN (SPARQL)**:
   - Add queries to `src/mcp_space_life_sciences/sparql_queries.py`
   - Use consistent PREFIX declarations
   - Document edge properties if using RDF reification

3. **For new tools**:
   - Add to `src/mcp_space_life_sciences/server.py`
   - Implement in `src/mcp_space_life_sciences/client.py`
   - Add tests to `tests/`
   - Update documentation

### Commit Message Guidelines

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Maintenance tasks

Examples:
- `feat: add drug-environment interaction query`
- `fix: correct SPARQL endpoint URL`
- `docs: update installation instructions`

### Pull Request Process

1. Update the README.md with details of changes if needed
2. Update documentation files as appropriate
3. Add your changes to the relevant section in CHANGELOG.md (create if needed)
4. The PR will be merged once reviewed and approved

### Questions?

- Open a GitHub Discussion for general questions
- Use Issues for specific bugs or feature requests
- Check existing documentation in `docs/` first

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Harassment, discrimination, or exclusionary comments
- Personal or political attacks
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of unacceptable behavior may be reported by contacting the project maintainers. All complaints will be reviewed and investigated.

## Attribution

This project integrates work from:
- **GeneLab** - NASA Ames Research Center
- **PrimeKG** - Zitnik Lab, Harvard Medical School
- **SPOKE-OKN** - Baranzini Lab, UCSF & RENCI

Please maintain proper attribution when contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- The project README
- Release notes
- Academic publications (where appropriate)

Thank you for contributing to space life sciences research! 🚀
