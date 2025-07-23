# Resume Screener API

An AI-powered resume screening API built with FastAPI and Google Gemini that intelligently analyzes resumes against job requirements.

## 🌟 Features

- **PDF Resume Parsing** - Automatically extracts text from PDF resumes
- **AI-Powered Analysis** - Uses Google Gemini AI to provide intelligent insights
- **Job Matching** - Compares resumes against specific job requirements
- **Structured Output** - Returns JSON with scores, strengths, concerns, and match percentage
- **RESTful API** - Clean, well-documented API endpoints
- **Fast Performance** - Processes resumes in seconds

## 🛠️ Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Google Gemini AI** - Advanced language model for intelligent analysis
- **PyPDF2** - PDF text extraction
- **Python 3.8+** - Core programming language
- **Uvicorn** - Lightning-fast ASGI server

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ct302/resume-screener.git
cd resume-screener
```

### 2. Set Up Environment

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Using the start script
python start.py

# Or directly with uvicorn
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

### Endpoints

#### `GET /`
Returns API information and status.

#### `GET /health`
Health check endpoint for monitoring.

#### `POST /screen-resume`
Analyzes a resume against job requirements.

**Request:**
- `file`: PDF file (multipart/form-data)
- `job_requirements`: Job description text (optional)

**Response:**
```json
{
  "score": 8,
  "summary": "Experienced full-stack developer with strong Python skills. Good match for the senior developer position.",
  "strengths": [
    "5+ years Python experience",
    "FastAPI and REST API expertise",
    "Strong cloud deployment knowledge"
  ],
  "concerns": [
    "Limited experience with Rust",
    "No mention of team leadership"
  ],
  "match_percentage": 75
}
```

## 🏗️ Architecture

```
resume-screener/
├── app.py              # Main application file
├── app_secure.py       # Secure version with env variables
├── requirements.txt    # Python dependencies
├── start.py           # Convenient startup script
├── usage_monitor.py   # Usage tracking utilities
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
├── Procfile          # Railway deployment config
└── README.md         # This file
```

## 🚀 Deployment

### Railway Deployment

This project is configured for easy deployment on Railway:

1. Connect your GitHub repository to Railway
2. Add `GEMINI_API_KEY` environment variable
3. Deploy! Railway will auto-detect the Python app

### Other Platforms

The API can be deployed on any platform that supports Python:
- Heroku
- Google Cloud Run
- AWS Lambda
- DigitalOcean App Platform

## 🔒 Security

- API keys are stored in environment variables
- `.env` files are excluded from version control
- Input validation on all endpoints
- Rate limiting ready (can be configured)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Charley Turner** - [GitHub Profile](https://github.com/ct302)

## 🙏 Acknowledgments

- Google Gemini team for the powerful AI model
- FastAPI for the excellent web framework
- The open-source community
