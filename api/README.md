# Human Body Measurements API

A FastAPI-based service for human body measurements using computer vision. This API provides endpoints to analyze images and extract body measurements with features like JWT authentication, rate limiting, caching, and comprehensive error handling.

## Features

- 🔐 **JWT Authentication** - Secure API access with token-based authentication
- 🚦 **Rate Limiting** - Configurable rate limiting to prevent abuse
- 💾 **Redis Caching** - Efficient caching for models and results
- 📊 **Structured Logging** - Comprehensive logging with structured data
- 🔄 **API Versioning** - Versioned API endpoints
- ⚡ **Graceful Failure** - Robust error handling and recovery
- 🐳 **Docker Support** - Easy deployment with Docker and Docker Compose
- 🧪 **Comprehensive Testing** - Full test suite with pytest
- 📚 **API Documentation** - Interactive docs with Swagger UI

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project directory**
   ```bash
   cd Human-Body-Measurements-using-Computer-Vision
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Manual Setup

1. **Install dependencies**
   ```bash
   cd api
   pip install -r requirements.txt
   ```

2. **Start Redis** (required for caching and rate limiting)
   ```bash
   docker run -d -p 6379:6379 redis:7-alpine
   ```

3. **Set environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Usage

### Authentication

1. **Register a new user**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/register" \
        -H "Content-Type: application/json" \
        -d '{
          "username": "testuser",
          "email": "test@example.com",
          "password": "testpassword"
        }'
   ```

2. **Login to get access token**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=testuser&password=testpassword"
   ```

### Body Measurements

#### Using Base64 Image

```bash
curl -X POST "http://localhost:8000/api/v1/measurements/analyze-base64" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "height": 72.0,
       "image_data": "base64_encoded_image_data"
     }'
```

#### Using File Upload

```bash
curl -X POST "http://localhost:8000/api/v1/measurements/analyze" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -F "height=72.0" \
     -F "image=@path/to/your/image.jpg"
```

### Response Format

```json
{
  "success": true,
  "measurements": {
    "height": 72.0,
    "waist": 35.61,
    "belly": 34.14,
    "chest": 40.16,
    "wrist": 6.75,
    "neck": 14.45,
    "arm_length": 22.27,
    "thigh": 22.34,
    "shoulder_width": 19.74,
    "hips": 40.63,
    "ankle": 8.52
  },
  "processing_time": 12.34,
  "model_version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Testing

### Run Tests

```bash
cd api
pytest tests/ -v
```

### Test Coverage

```bash
pytest tests/ --cov=app --cov-report=html
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `RATE_LIMIT_REQUESTS` | Rate limit requests per window | `10` |
| `RATE_LIMIT_WINDOW` | Rate limit window in seconds | `60` |
| `LOG_LEVEL` | Logging level | `INFO` |

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user info

### Measurements
- `POST /api/v1/measurements/analyze` - Analyze with file upload
- `POST /api/v1/measurements/analyze-base64` - Analyze with base64 image
- `GET /api/v1/measurements/health` - Measurement service health

### System
- `GET /` - Root endpoint
- `GET /health` - System health check
- `GET /docs` - API documentation
- `GET /redoc` - ReDoc documentation

## Postman Collection

Import the `postman_collection.json` file into Postman to test all endpoints with pre-configured requests.

## Error Handling

The API returns structured error responses:

```json
{
  "success": false,
  "error": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Common Error Codes

- `HTTP_400` - Bad Request
- `HTTP_401` - Unauthorized
- `HTTP_422` - Validation Error
- `HTTP_429` - Rate Limit Exceeded
- `HTTP_500` - Internal Server Error

## Rate Limiting

- **Default**: 10 requests per minute per IP
- **Measurement endpoints**: 5-10 requests per minute per user
- **Headers**: Rate limit info included in response headers

## Caching

- **Model caching**: Models are cached in Redis for 1 hour
- **Result caching**: Measurement results cached for 30 minutes
- **Cache keys**: Based on image hash and parameters

## Logging

Structured JSON logging includes:
- Request/response details
- Processing times
- Error information
- User actions
- Performance metrics

## Development

### Project Structure

```
api/
├── app/
│   ├── api/v1/          # API routes
│   ├── core/            # Core functionality
│   ├── middleware/      # Custom middleware
│   ├── schemas/         # Pydantic models
│   └── services/        # Business logic
├── tests/               # Test suite
├── requirements.txt     # Dependencies
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

### Adding New Endpoints

1. Create route in `app/api/v1/`
2. Add schema in `app/schemas/`
3. Implement service in `app/services/`
4. Add tests in `tests/`
5. Update documentation

## Production Deployment

### Security Considerations

1. **Change default secret key**
2. **Use HTTPS**
3. **Configure CORS properly**
4. **Set up proper Redis authentication**
5. **Use environment-specific configurations**
6. **Enable request logging and monitoring**

### Performance Optimization

1. **Use Redis clustering for high availability**
2. **Implement connection pooling**
3. **Add request/response compression**
4. **Use CDN for static assets**
5. **Monitor and optimize database queries**

## Troubleshooting

### Common Issues

1. **Redis connection failed**
   - Check Redis is running
   - Verify connection settings

2. **Model loading failed**
   - Ensure model files are present
   - Check file permissions

3. **Rate limiting issues**
   - Check Redis connection
   - Verify rate limit configuration

4. **Authentication errors**
   - Verify JWT secret key
   - Check token expiration

## License

This project is licensed under the MIT License.

