import uvicorn
from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/fdp")
def fils_de_pute():
    return {"response": "Fils de pute."}


uvicorn.run(app)