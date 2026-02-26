from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pdf_service import extract_text_from_pdf
from deterministic_engine import deterministic_evaluation
from models import EvaluationResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# HEALTH CHECK
# ----------------------------

@app.get("/")
def health():
    return {"status": "ok"}


# ----------------------------
# EVALUATION ENDPOINT
# ----------------------------

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(
    resume_file: UploadFile = File(None),
    resume_text: str = Form(None),
    github_link: str = Form(None),
    linkedin_link: str = Form(None),
):
    # 🔒 Validation
    if not resume_file and not resume_text:
        raise HTTPException(
            status_code=400,
            detail="Resume file or resume text must be provided."
        )

    # Extract resume content
    if resume_file:
        file_bytes = await resume_file.read()
        extracted_text = extract_text_from_pdf(file_bytes)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from PDF."
            )
    else:
        extracted_text = resume_text.strip()

    # Run deterministic engine
    result = deterministic_evaluation(extracted_text)

    return result