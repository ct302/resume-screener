# API Documentation

## Base URL

```
http://localhost:8000
```

For production deployments, replace with your actual domain.

## Authentication

Currently, the API does not require authentication. Future versions may include API key authentication for production use.

## Endpoints

### 1. Root Endpoint

**GET /**

Returns basic API information and status.

#### Response

```json
{
  "message": "Resume Screener API - AI-powered resume analysis",
  "docs": "Visit /docs for interactive API documentation",
  "status": "ready",
  "model": "gemini-1.5-flash"
}
```

### 2. Health Check

**GET /health**

Checks if the API and AI model are functioning properly.

#### Response

```json
{
  "status": "healthy",
  "api": "google-gemini",
  "model": "gemini-1.5-flash",
  "test": "API is working"
}
```

### 3. Screen Resume

**POST /screen-resume**

Main endpoint for analyzing resumes against job requirements.

#### Request

- **Method:** POST
- **Content-Type:** multipart/form-data

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File (PDF) | Yes | The resume file to analyze |
| job_requirements | String | No | Job description or requirements to match against |

#### Example Request

```bash
curl -X POST \
  http://localhost:8000/screen-resume \
  -F "file=@resume.pdf" \
  -F "job_requirements=Looking for a senior Python developer with 5+ years experience"
```

#### Response

```json
{
  "score": 8,
  "summary": "Strong Python developer with 7 years of experience. Excellent match for senior position with proven track record.",
  "strengths": [
    "7 years of Python development experience",
    "Experience with FastAPI and modern web frameworks",
    "Strong background in cloud technologies (AWS, GCP)"
  ],
  "concerns": [
    "No mention of team leadership experience",
    "Limited front-end development skills"
  ],
  "match_percentage": 85
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| score | Integer (1-10) | Overall candidate score |
| summary | String | 2-sentence summary of the candidate |
| strengths | Array[String] | Key strengths identified |
| concerns | Array[String] | Potential concerns or gaps |
| match_percentage | Integer (0-100) | How well the resume matches requirements |

### 4. List Models

**GET /list-models**

Lists all available AI models that can be used for analysis.

#### Response

```json
{
  "available_models": [
    {
      "name": "gemini-1.5-flash",
      "display_name": "Gemini 1.5 Flash",
      "description": "Fast, efficient model for quick analysis"
    },
    {
      "name": "gemini-1.0-pro",
      "display_name": "Gemini 1.0 Pro",
      "description": "Balanced model for general use"
    }
  ]
}
```

### 5. API Info

**GET /api-info**

Provides detailed information about the API capabilities.

#### Response

```json
{
  "api": "Google Gemini",
  "model": "gemini-1.5-flash",
  "model_status": "working",
  "features": [
    "PDF resume parsing",
    "AI-powered analysis",
    "Job requirement matching",
    "Strength and concern identification",
    "Compatibility scoring"
  ],
  "endpoints": {
    "/": "API information",
    "/docs": "Interactive API documentation",
    "/health": "Health check",
    "/screen-resume": "Analyze a resume",
    "/list-models": "List available AI models"
  }
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

### Common Error Responses

#### 400 Bad Request

```json
{
  "error": "Invalid file format",
  "message": "Please upload a PDF file",
  "tip": "Make sure the file is a valid PDF"
}
```

#### 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 500 Internal Server Error

```json
{
  "error": "Model initialization failed",
  "message": "Failed to initialize AI model",
  "tip": "Check /list-models for available models"
}
```

## Rate Limiting

The Google Gemini API allows:
- 60 requests per minute
- 1,500 free requests per day

## Best Practices

1. **File Size**: Keep PDF files under 10MB for optimal performance
2. **Job Requirements**: Provide detailed job requirements for better matching accuracy
3. **Error Handling**: Always check the response status and handle errors appropriately
4. **Batch Processing**: For multiple resumes, process them sequentially to avoid rate limits

## Example Integration

### Python

```python
import requests

def screen_resume(pdf_path, job_requirements=""):
    url = "http://localhost:8000/screen-resume"
    
    with open(pdf_path, 'rb') as f:
        files = {'file': f}
        data = {'job_requirements': job_requirements}
        response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Usage
result = screen_resume("resume.pdf", "Senior Python Developer")
print(f"Score: {result['score']}/10")
print(f"Match: {result['match_percentage']}%")
```

### JavaScript

```javascript
async function screenResume(file, jobRequirements = "") {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_requirements', jobRequirements);

  const response = await fetch('http://localhost:8000/screen-resume', {
    method: 'POST',
    body: formData
  });

  if (response.ok) {
    return await response.json();
  } else {
    throw new Error(`Error: ${response.status}`);
  }
}
```

## Support

For issues or questions, please open an issue on the GitHub repository.
