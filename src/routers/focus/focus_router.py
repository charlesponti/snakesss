from typing import List

from chromadb.api.types import Document
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from lib.clients.chromadb_service import vector_db
from lib.file_service import FileRepository
from lib.logger import logger

from src.routers.focus.focus_service import analyze_user_input

focus_router = APIRouter()


@focus_router.post("/focus")
def focus(transcript: str, model: str = "llama3-70b-8192"):
    """
    Returns notes structure content as well as total tokens and total time for generation.
    """
    if not transcript.strip():
        return None, {"error": "No tasks provided in the transcript"}

    try:
        analysis = analyze_user_input(transcript)
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f" ********* ERROR IN USER PROMPT ********: {e} ***** ")
        return None, {"error": str(e)}


@focus_router.get("/test")
def test():
    test_user_input = FileRepository.get_file_contents("src/prompts/test_user_input.md")
    analysis = analyze_user_input(test_user_input)
    return {"analysis": analysis}


class Query(BaseModel):
    query: str


@focus_router.post("/tasks/search/")
async def search_tasks(query: Query):
    # Embed the query using the same embeddings model
    try:
        search_results = vector_db.similarity_search(query.query, k=5)  # Return top 5 matches
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during search")

    # Retrieve the task descriptions for the matched results
    matching_tasks: List[str] = []
    for result in search_results:
        task_id = result.metadata["id"]
        task = next((task for task in search_results if task.id == task_id), None)
        if task:
            matching_tasks.append(task.page_content)

    if not matching_tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    return {"matching_tasks": matching_tasks}
