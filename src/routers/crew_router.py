from fastapi import APIRouter
from pydantic import BaseModel
from src.routers.crews.crew import TravelCrew

app = APIRouter(prefix="/crew")


class TravelInput(BaseModel):
    location: str


@app.post("/travel")
async def crew_chat(input: TravelInput):
    trip_plan_crew = TravelCrew().trip_plan_crew()
    response = trip_plan_crew.kickoff(inputs={"location": input.location})

    return {"content": response}
