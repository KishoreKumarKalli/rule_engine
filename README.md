# Rule Engine with AST

A simple rule engine application that uses Abstract Syntax Trees (AST) to evaluate business rules. The system allows for dynamic creation and evaluation of rules based on user attributes.

## Features

- Create and evaluate complex business rules
- Web interface for rule creation and testing
- REST API endpoints for integration
- Support for multiple operators (AND, OR, >, <, =, >=, <=, !=)
- Error handling and validation
- Basic security implementations

## Installation

### Prerequisites
- Python 3.8 or higher
- Modern web browser
- Git (optional)

### Quick Start
1. Clone or download the repository
2. Run the setup script:
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m uvicorn app:app --reload
```

## Usage

1. Access the web interface at `http://localhost:8000`
2. Create a rule using the syntax:
```
(age > 30 AND department = 'Sales') OR (experience >= 5)
```
3. Test with sample data:
```json
{
    "age": 35,
    "department": "Sales",
    "experience": 3
}
```

## API Documentation

### Create Rule
```http
POST /api/rules/create
Content-Type: application/json

{
    "rule_string": "(age > 30 AND department = 'Sales')"
}
```

### Evaluate Rule
```http
POST /api/rules/evaluate
Content-Type: application/json

{
    "rule": {
        // Rule AST structure
    },
    "data": {
        "age": 35,
        "department": "Sales"
    }
}
```

## Non-Functional Considerations

### Security
1. **Input Validation**
   - All rule inputs are sanitized and validated
   - JSON payload size limits implemented
   - No direct database queries from rule evaluation

2. **Authentication & Authorization** (To be implemented)
   - JWT-based authentication
   - Role-based access control
   - API key requirements for programmatic access

3. **Data Protection**
   - CORS protection implemented
   - XSS prevention in frontend
   - CSRF protection (to be implemented)

### Performance
1. **Optimization**
   - AST evaluation is optimized for minimal traversal
   - Rule parsing is cached where possible
   - Static files are served with caching headers

2. **Scalability**
   - Stateless design allows horizontal scaling
   - Async operations for improved concurrency
   - Database connection pooling (when implemented)

3. **Monitoring** (To be implemented)
   - Performance metrics collection
   - Error rate tracking
   - Response time monitoring

### Reliability
1. **Error Handling**
   - Comprehensive exception handling
   - Graceful degradation
   - Clear error messages

2. **Logging**
   - Request/response logging
   - Error logging with stack traces
   - Performance metric logging

### Maintainability
1. **Code Quality**
   - Type hints used throughout
   - Documentation strings for all functions
   - Consistent code formatting (flake8 compliant)

2. **Testing**
   - Unit tests for core functionality
   - Integration tests for API endpoints
   - Frontend component tests

## Development Roadmap

### Phase 1 (Current)
- ✓ Basic rule creation and evaluation
- ✓ Web interface
- ✓ Core API endpoints

### Phase 2 (Planned)
- [ ] Database integration
- [ ] User authentication
- [ ] Rule templates
- [ ] Advanced operators

### Phase 3 (Future)
- [ ] Rule versioning
- [ ] Audit logging
- [ ] Performance monitoring
- [ ] API rate limiting

## Testing

```bash
# Run unit tests
python -m pytest tests/unit

# Run integration tests
python -m pytest tests/integration

# Run with coverage
python -m pytest --cov=app tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Support

For issues and feature requests, please create an issue on GitHub.