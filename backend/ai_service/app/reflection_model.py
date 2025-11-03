import ollama, json, re
from app.data import SECTION_WEIGHTS

def get_reflection_score(text_sections: dict) -> float:
    prompt = f"""
    You are an expert evaluator of reflective writing. 
    Your task is to analyze a reflection divided into sections and score **each section separately**
    on how well it demonstrates introspection, reasoning, and personal growth.

    Return your answer ONLY as valid JSON in this exact format:
    {{
    "title": <int>,
    "contextDescription": <int>,
    "intendedGoal": <int>,
    "whatHappened": <int>,
    "whyItFailed": <int>,
    "lessonLearned": <int>,
    "adviceToOthers": <int>
    }}

    Each value must be an integer from 0 to 100.

    --------------------------------------------------------------------
    ### Scoring Philosophy
    A high-quality reflection is honest, analytical, and self-aware.
    It connects causes and effects, extracts lessons, and shows emotional maturity.
    Length and richness matter: deeper reasoning usually requires more words,
    but verbosity without meaning should not raise the score.

    --------------------------------------------------------------------
    ### Quality Levels (with examples)

    #### Very Low (0-25)
    • Superficial or dismissive tone.  
    • No responsibility taken.  
    • No reasoning or lessons.  
    **Example:**  
    > "I failed because my teammates didn’t help and the teacher was unfair."  
    → Blames others, zero learning insight.  

    #### Low (26-50)
    • Minimal reflection, vague cause.  
    • Mentions events but not reasoning.  
    **Example:**  
    > "I didn’t prepare enough for the exam, but next time I’ll study more."  
    → Admits issue, but gives no insight into *why* or *how* to improve.  

    #### Medium (51-75)
    • Some self-awareness and reasoning.  
    • Basic lessons extracted, modest emotional insight.  
    **Example:**  
    > "I underestimated how long the project would take. I learned to plan earlier next time."  
    → Shows accountability and a simple lesson.  

    #### High (76-100)
    • Deeply introspective and emotionally mature.  
    • Explains causes, consequences, and growth.  
    • Offers transferable insight or advice.  
    **Example:**  
    > "I procrastinated on my thesis because I feared judgment. Realizing that helped me address my anxiety and break tasks into small wins."  
    → Shows cause-effect reasoning, emotional growth, and actionable insight.  

    --------------------------------------------------------------------
    ### Section-Specific Guidance

    | Section | Focus | Special considerations |
    |----------|-------|------------------------|
    | **Title** | Does it reflect the core learning or theme? | Very short but still reveals awareness. |
    | **Context Description** | Does it set up the situation clearly? | Shows understanding of background and stakes. |
    | **Intended Goal** | Does it reveal purpose and motivation? | Links goal to personal values or expectations. |
    | **What Happened** | Is the narration coherent and self-aware? | Includes cause–effect, not excuses. |
    | **Why It Failed** | Does the author analyze mistakes logically? | Avoids blame, focuses on reasoning. |
    | **Lesson Learned** | Does it express concrete insight or changed mindset? | The most critical metric; depth counts heavily. |
    | **Advice To Others** | Does it generalize learning into useful guidance? | Shows empathy and transfer of knowledge. |

    --------------------------------------------------------------------
    ### Length and Richness Adjustment
    - Under 40 words → usually shallow, cap at 40 max.  
    - 40–150 words → normal range, no adjustment.  
    - 150–300 words → often rich; higher potential if coherent.  
    - Over 300 words → check for rambling; reward only if focused.  

    --------------------------------------------------------------------
    ### Evaluation Instructions
    1. Read each section carefully.  
    2. Assign an integer score (0–100) reflecting its reflective quality.  
    3. Penalize empty or missing sections by giving **0**.  
    4. Use consistent calibration across all sections.  
    5. Return ONLY the JSON object, no commentary or markdown.  

    --------------------------------------------------------------------
    ### Sections to Evaluate

    Title:
    {text_sections["title"]}

    Context Description:
    {text_sections["contextDescription"]}

    Intended Goal:
    {text_sections["intendedGoal"]}

    What Happened:
    {text_sections["whatHappened"]}

    Why It Failed:
    {text_sections.get("whyItFailed", "")}

    Lesson Learned:
    {text_sections.get("lessonLearned", "")}

    Advice To Others:
    {text_sections.get("adviceToOthers", "")}

    Remember: only output JSON with numeric values.
    """


    

    try:
        res = ollama.chat(
            model="mistral:7b-instruct-v0.2-q8_0",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0, "num_ctx": 4096, "num_predict": 600}
        )

        raw = res["message"]["content"].strip()
        raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()

        section_scores = json.loads(raw)
        print("Section-level scores:", section_scores)

        weighted_sum = 0
        total_weight = 0
        for section, weight in SECTION_WEIGHTS.items():
            if section_scores.get(section) is not None:
                weighted_sum += section_scores[section] * weight
                total_weight += weight

        overall_reflection_score = round(weighted_sum / total_weight, 2)
        return {"section_scores": section_scores, "overall_score": overall_reflection_score}

    except Exception as e:
        print("Sectional reflection scoring error:", e)
        return {"section_scores": {}, "overall_score": 0.0}
