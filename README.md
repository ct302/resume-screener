# Resume Screener API

[![Live Demo](https://img.shields.io/badge/demo-live-green)](https://web-production-f004.up.railway.app)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered resume screening API built with FastAPI and Google Gemini that intelligently analyzes resumes against job requirements.

🔗 **Live Demo**: https://web-production-f004.up.railway.app  
📚 **API Docs**: https://web-production-f004.up.railway.app/docs

## 🌟 Features

- **PDF Resume Parsing** - Automatically extracts text from PDF resumes
- **AI-Powered Analysis** - Uses Google Gemini AI to provide intelligent insights
- **Job Matching** - Compares resumes against specific job requirements
- **Structured Output** - Returns JSON with scores, strengths, concerns, and match percentage
- **RESTful API** - Clean, well-documented API endpoints
- **Fast Performance** - Processes resumes in seconds
- **Bulk Processing** - Screen multiple resumes at once

## 🛠️ Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Google Gemini AI** - Advanced language model for intelligent analysis
- **PyPDF2** - PDF text extraction
- **Python 3.8+** - Core programming language
- **Uvicorn** - Lightning-fast ASGI server
- **Railway** - Cloud deployment platform

## 🚀 Try It Now

Test the live API at: https://web-production-f004.up.railway.app/docs

```bash
# Quick test with curl
curl -X POST https://web-production-f004.up.railway.app/screen-resume \
  -F "file=@your-resume.pdf" \
  -F "job_requirements=Python developer with FastAPI experience"
```

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## 💻 Local Development

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

- **Live API Docs**: https://web-production-f004.up.railway.app/docs
- **Local Docs**: http://localhost:8000/docs

### Main Endpoints

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

#### `POST /bulk-screen`
Process multiple resumes at once (up to 10).

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete endpoint details.

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
├── LICENSE            # MIT License
├── API_DOCUMENTATION.md # Detailed API docs
└── README.md         # This file
```

## 🚀 Deployment

### Live Deployment

This API is currently deployed and live at: https://web-production-f004.up.railway.app

### Deploy Your Own Instance

#### Railway (Recommended)

1. Fork this repository
2. Sign up at [Railway.app](https://railway.app)
3. Create new project → Deploy from GitHub
4. Select your forked repository
5. Add environment variable: `GEMINI_API_KEY`
6. Deploy! Your API will be live in minutes

#### Other Platforms

The API can be deployed on any platform that supports Python:
- Heroku
- Google Cloud Run
- AWS Lambda
- DigitalOcean App Platform

## 🔒 Security

- API keys are stored in environment variables
- `.env` files are excluded from version control
- Input validation on all endpoints
- HTTPS enforced in production
- Rate limiting via Google Gemini API (60 req/min)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Charley Turner** - [GitHub Profile](https://github.com/ct302)

## 🙏 Acknowledgments

- Google Gemini team for the powerful AI model
- FastAPI for the excellent web framework
- Railway for seamless deployment
- The open-source community

---

⭐ If you find this project useful, please consider giving it a star!
