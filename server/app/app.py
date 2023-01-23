from .utils import util
from .controller import board, task, webhooks
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


log = util.getLog(__name__)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(board.router, tags=['Boards'], prefix='/api/boards')
app.include_router(task.router, tags=['Tasks'], prefix='/api/tasks')
app.include_router(webhooks.router, tags=['Webhooks'], prefix='/api/webhooks')


@app.get("/")
def root():
    log.info("API endpoint for is alive called")
    return {"message": "server is alive!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000,log_level="debug", debug=True)