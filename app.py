from fastapi import FastAPI
from pydantic import BaseModel, Field
from google import genai

app = FastAPI(title="AI Code Debugger API")

# Replace with your Gemini API key
client = genai.Client(api_key="GEMINI_API_KEY")  


class DebugRequest(BaseModel):
    language: str = Field(
        min_length=1,
        max_length=30,
        description="Programming Language"
    )

    code: str = Field(
        min_length=10,
        max_length=10000,
        description="Source Code"
    )


@app.get("/")
def home():
    return {
        "message": "AI Code Debugger Backend is Running"
    }


@app.post("/debug")
def debug_code(req: DebugRequest):

    prompt = f"""
You are an expert software engineer and code reviewer.

Programming Language:
{req.language}

Source Code:
{req.code}

Analyze the code carefully.

Perform ALL of the following tasks:

1. Identify every syntax error.
2. Identify every logical error.
3. Identify possible runtime errors.
4. Explain each error in simple English.
5. Mention the error type (SyntaxError, TypeError, NullPointerException, etc.).
6. Provide the corrected code.
7. Explain why the corrected code works.
8. Show the expected output after correction.
9. Suggest best coding practices.
10. If there are no errors, clearly state that the code is correct and suggest improvements.

Format the response exactly like this:

## Error Type

## Error Explanation

## Corrected Code

## Why This Fix Works

## Expected Output

## Best Practices
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "language": req.language,
        "result": response.text
    }
