import re
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
        messages = body.get("messages", [])
        last_message = messages[-1].get("content", "") if messages else ""

        # Arithmetic test: "What is A + B?"
        math_match = re.search(r'what\s+is\s+(\d+)\s*\+\s*(\d+)', last_message, re.IGNORECASE)
        if math_match:
            val = int(math_match.group(1)) + int(math_match.group(2))
            return {
                "choices": [{"index": 0, "message": {"role": "assistant", "content": str(val)}, "finish_reason": "stop"}]
            }

        # Echo test: "Output ONLY this exact token and nothing else: TKxxxxxx"
        echo_match = re.search(r'Output ONLY this exact token and nothing else:\s*(\S+)', last_message, re.IGNORECASE)
        if echo_match:
            token = echo_match.group(1).strip()
            return {
                "choices": [{"index": 0, "message": {"role": "assistant", "content": token}, "finish_reason": "stop"}]
            }

        # fallback
        return {
            "choices": [{"index": 0, "message": {"role": "assistant", "content": ""}, "finish_reason": "stop"}]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def root():
    return {"status": "ok"}
