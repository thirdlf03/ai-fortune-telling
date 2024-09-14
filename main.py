from fastapi import FastAPI, Request, status, Form
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn

key=""
client = OpenAI(api_key=key)

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost",
                   "http://127.0.0.1",
                   "http://127.0.0.1:8000"
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/result", response_class=HTMLResponse)
async def GetResult(request:Request, name: str = Form(), blood_type: str = Form(), category: str = Form()):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたはプロの占い師です。"},
            {"role": "system", "content": "与えられた情報からユーザーのラッキーカラーを占ってください"},
            {"role": "system", "content": "出力は、~さんのラッキーカラーは~色です。から始めてください"},
            {
                "role": "user",
                "content": f"名前は{name}で血液型は{blood_type}です。{category}について答えてください。"
            }
        ]
    )
    return templates.TemplateResponse("result.html", {"request": request, "result": completion.choices[0].message.content})

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
