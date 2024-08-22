from pydantic import BaseModel
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import uvicorn

key=""
client = OpenAI(api_key=key)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/")
async def GetResult(name, blood_type):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたはプロの占い師です。"},
            {"role": "system", "content": "与えられた情報からユーザーのラッキーカラーを占ってください"},
            {"role": "system", "content": "出力は、~さんのラッキーカラーは~色です。から始めてください"},
            {
                "role": "user",
                "content": f"名前は{name}で血液型は{blood_type}です。"
            }
        ]
    )
    return {"message" : completion.choices[0].message.content}

if __name__ == '__main__':
    uvicorn.run("main.app", port=8000, reload=True)