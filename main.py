from api.rest_server import app
import uvicorn


def main():
    uvicorn.run(app)


if __name__ == "__main__":
    main()
