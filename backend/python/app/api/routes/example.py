from fastapi import APIRouter

route = APIRouter(prefix="/analysis")

# @router.post("/", response_description="Add new task")
# async def create_task(request: Request, task: TaskModel = Body(...)):
#     task = jsonable_encoder(task)
#     new_task = await request.app.mongodb["tasks"].insert_one(task)
#     created_task = await request.app.mongodb["tasks"].find_one(
#         {"_id": new_task.inserted_id}
#     )

#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)