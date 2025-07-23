from fastapi import FastAPI, UploadFile, File, Form
import google.generativeai as genai
import PyPDF2
import io
import json
import re
import os
from dotenv import load_dotenv
# from usage_monitor import UsageMonitor  # Uncomment to track usage

# Load environment variables
load_dotenv()

app = FastAPI(title="Resume Screener API - Powered by Gemini", version="1.0.0")

# Configure Gemini with your API key from environment variable
# IMPORTANT: Create a .env file with GEMINI_API_KEY=your-actual-key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize usage monitor (uncomment to track API usage and costs)
# monitor = UsageMonitor()

# Try to initialize the model with fallbacks
try:
    # First try the latest free model
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
        "message": "Resume Screener API - Powered by Google Gemini (FREE!)",
        "docs": "Visit /docs for interactive API documentation",
        "status": "ready" if model else "error",
        "model": MODEL_NAME
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "model": MODEL_NAME}

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
        
        # Track usage (uncomment if using monitor)
        # daily_count, cost = monitor.track_request()
        
        # The magic prompt for Gemini
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
        
        # Clean up response (remove markdown if any)
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Try to parse as JSON
        try:
            result = json.loads(response_text)
        except:
            # Fallback: try to extract JSON with regex
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Last resort: return raw response
                result = {
                    "score": 5,
                    "summary": "Analysis completed but format unclear. Check raw response.",
                    "strengths": ["See raw response"],
                    "concerns": ["JSON parsing failed"],
                    "match_percentage": 50,
                    "raw_response": response_text
                }
        
        # Print usage stats every 100 requests (uncomment if using monitor)
        # if daily_count % 100 == 0:
        #     monitor.print_summary()
        
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "tip": "Make sure the file is a valid PDF and try again"
        }

@app.post("/bulk-screen")
async def bulk_screen(
    files: list[UploadFile] = File(...),
    job_requirements: str = Form("")
):
    """Process multiple resumes at once (up to 10)"""
    if len(files) > 10:
        return {"error": "Maximum 10 resumes per batch"}
    
    results = []
    for file in files:
        result = await screen_resume(file, job_requirements)
        results.append({
            "filename": file.filename,
            "result": result
        })
    
    return {
        "processed": len(results),
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️  WARNING: GEMINI_API_KEY not found in environment variables!")
        print("Create a .env file with: GEMINI_API_KEY=your-key-here")
    uvicorn.run(app, host="0.0.0.0", port=8000)
