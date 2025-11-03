from fastapi import FastAPI, HTTPException, Depends, Header, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import os
from app.reflection_model import get_reflection_score
from app.moderation_model import get_offense_score
from app.utils import sanitize_text


app = FastAPI(title="HIWIF AI Service")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# ---------- Models ----------
class PostInput(BaseModel):
    title: str
    contextDescription: str
    whyItFailed: str

# ---------- Auth Middleware ----------
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("INTERNAL_AI_API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
# ---------- Rate Limit Handler ----------
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
def analyze_post(request: Request, data: PostInput):
    text_sections = {
        "title": sanitize_text(getattr(data, "title", "")),
        "contextDescription": sanitize_text(getattr(data, "contextDescription", "")),
        "intendedGoal": sanitize_text(getattr(data, "intendedGoal", "")),
        "whatHappened": sanitize_text(getattr(data, "whatHappened", "")),
        "whyItFailed": sanitize_text(getattr(data, "whyItFailed", "") or ""),
        "lessonLearned": sanitize_text(getattr(data, "lessonLearned", "") or ""),
        "adviceToOthers": sanitize_text(getattr(data, "adviceToOthers", "") or ""),
    }

    reflection_score = get_reflection_score(text_sections)
    offensive_score = get_offense_score(
        ". ".join(text_sections.values())
    )

    return {
        "offensive": offensive_score > 0.5,
        "offensive_score": offensive_score,
        "section_scores": reflection_score["section_scores"],
        "reflection_score": reflection_score["overall_score"]
    }
