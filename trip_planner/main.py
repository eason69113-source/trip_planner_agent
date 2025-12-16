from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from trip_planner_agent import get_trip_planner_agent
from schemas import TripRequest, TripPlanResponse
import uvicorn

app = FastAPI(title="AI旅行助手", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = get_trip_planner_agent()

@app.post("/api/v1/trip/plan", response_model=TripPlanResponse)
async def plan_trip(request: TripRequest):
    try:
        await planner.initialize()
        plan = await planner.plan_trip(request)
        return TripPlanResponse(success=True, message="规划成功", data=plan)
    except Exception as e:
        return TripPlanResponse(success=False, message=str(e))
    
@app.get("/")
async def root():
    return {"message": "AI旅行规划系统已启动！前端地址：http://127.0.0.1:5500"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)