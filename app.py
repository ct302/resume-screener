from fastapi import FastAPI, UploadFile, File, Form
import google.generativeai as genai
import PyPDF2
import io
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Resume Screener API", version="1.0.0")

# Configure Gemini with API key from environment variable
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Try to initialize the model with fallbacks
try:
    # First try the latest model
    model = genai.GenerativeModel('gemini-1.5-flash')
    MODEL_NAME = 'gemini-1.5-flash'
except:
    try:
        # Fallback to Pro model
        model = genai.GenerativeModel('gemini-1.0-pro')
        MODEL_NAME = 'gemini-1.0-pro'
    except:
        # Last resort - list available models
        MODEL_NAME = 'unknown'
        model = None

@app.get("/")
def read_root():
    return {
        "message": "Resume Screener API - AI-powered resume analysis",
        "docs": "Visit /docs for interactive API documentation",
        "status": "ready" if model else "error",
        "model": MODEL_NAME
    }

@app.get("/list-models")
def list_models():
    """List all available Gemini models"""
    try:
        models = genai.list_models()
        available = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                available.append({
                    "name": m.name.split('/')[-1],  # Just the model name
                    "display_name": m.display_name,
                    "description": m.description[:200]
                })
        return {"available_models": available}
    except Exception as e:
        return {"error": str(e)}

@app.post("/screen-resume")
async def screen_resume(
    file: UploadFile = File(...),
    job_requirements: str = Form("")
):
    """
    Analyze a resume against job requirements using AI.
    
    Args:
        file: PDF file of the resume
        job_requirements: Job description or requirements to match against
    
    Returns:
        JSON with score, summary, strengths, concerns, and match percentage
    """
    if not model:
        return {
            "error": "Model not initialized",
            "message": "Please check /list-models to see available models",
            "tip": "Update app.py with a working model name"
        }
    
    try:
        # Extract text from PDF
        pdf_content = await file.read()
        pdf_file = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        resume_text = ""
        for page in pdf_file.pages:
            resume_text += page.extract_text()
        
        # Limit resume text to prevent token issues
        resume_text = resume_text[:3000]
        
        # Create the analysis prompt
        prompt = f"""
        You are an expert resume screener. Analyze this resume against the job requirements.
        
        Resume: {resume_text}
        
        Job Requirements: {job_requirements if job_requirements else "General screening - look for red flags and strengths"}
        
        Provide your analysis in EXACTLY this JSON format (no markdown, just pure JSON):
        {{
            "score": <integer from 1-10>,
            "summary": "<2-sentence summary of the candidate>",
            "strengths": ["<strength1>", "<strength2>", "<strength3>"],
            "concerns": ["<concern1>", "<concern2>"],
            "match_percentage": <integer from 0-100>
        }}
        
        Be harsh but fair. Look for real experience, not just keywords.
        Only return the JSON, nothing else.
        """
        
        # Generate response with Gemini
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Clean the response - Gemini sometimes adds markdown formatting
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON response
        try:
            result = json.loads(response_text)
            # Ensure all required fields exist
            required_fields = ["score", "summary", "strengths", "concerns", "match_percentage"]
            for field in required_fields:
                if field not in result:
                    if field == "summary":
                        result[field] = "Analysis completed"
                    elif field in ["strengths", "concerns"]:
                        result[field] = []
                    else:
                        result[field] = 0
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured response
            return {
                "score": 5,
                "summary": "Resume processed successfully but response parsing failed.",
                "strengths": ["Resume uploaded successfully"],
                "concerns": ["Analysis format error - try again"],
                "match_percentage": 50,
                "raw_response": response_text[:500],
                "tip": "The AI response wasn't in JSON format. Try again."
            }
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to process resume",
            "model": MODEL_NAME,
            "tip": "Check /list-models for available models"
        }

# Health check endpoint
@app.get("/health")
def health_check():
    """Check if the API and AI model are working properly"""
    if not model:
        return {
            "status": "error",
            "message": "Model not initialized",
            "tip": "Check /list-models"
        }
    
    try:
        # Quick test to see if Gemini is responding
        test_response = model.generate_content("Say 'API is working'")
        return {
            "status": "healthy", 
            "api": "google-gemini",
            "model": MODEL_NAME,
            "test": test_response.text[:50]
        }
    except Exception as e:
        return {
            "status": "error",
            "api": "google-gemini",
            "model": MODEL_NAME,
            "error": str(e)
        }

@app.get("/api-info")
def api_info():
    """Get information about the API and its capabilities"""
    return {
        "api": "Google Gemini",
        "model": MODEL_NAME,
        "model_status": "working" if model else "not initialized",
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
