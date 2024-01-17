import uvicorn
from api.rest_server import app

if __name__ == "__main__":
    uvicorn.run(app)
