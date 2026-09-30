from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.ai import generate_nutrition, generate_workout, update_workout
from app.database import delete_user, get_all_users, get_user, save_plan, save_user, update_plan
from app.schemas import UserInput

router=APIRouter(); templates=Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request,name="index.html",context={"error":None})

@router.post("/generate-workout")
def generate_workout_route(request: Request,user_id:str=Form(...),name:str=Form(...),age:int=Form(...),weight:str=Form(...),goal:str=Form(...),intensity:str=Form(...)):
    try: data=UserInput(user_id=user_id,name=name,age=age,weight=weight,goal=goal,intensity=intensity).model_dump()
    except Exception as exc: return templates.TemplateResponse(request=request,name="index.html",context={"error":f"Please check your details: {exc}"},status_code=400)
    if get_user(user_id): return templates.TemplateResponse(request=request,name="index.html",context={"error":"This User ID already exists. Please use another ID."},status_code=400)
    save_user(data); plan=generate_workout(data); nutrition=generate_nutrition(data); save_plan(user_id,plan,nutrition)
    return templates.TemplateResponse(request=request,name="result.html",context={"user":data,"workout_plan":plan,"nutrition_tip":nutrition,"message":None})

@router.get("/feedback")
def feedback_page(request: Request):
    return templates.TemplateResponse(request=request,name="feedback.html",context={"error":None,"user_id":""})

@router.post("/submit-feedback")
def submit_feedback(request: Request,user_id:str=Form(...),feedback:str=Form(...)):
    user=get_user(user_id)
    if not user: return templates.TemplateResponse(request=request,name="feedback.html",context={"error":"User ID not found.","user_id":user_id},status_code=404)
    plan=update_workout(user.original_plan,feedback); update_plan(user_id,plan,feedback)
    data={"user_id":user.user_id,"name":user.name,"age":user.age,"weight":user.weight,"goal":user.goal,"intensity":user.intensity}
    return templates.TemplateResponse(request=request,name="result.html",context={"user":data,"workout_plan":plan,"nutrition_tip":user.nutrition_tip,"message":"Your workout plan was updated successfully!"})

@router.get("/view-all-users")
def view_all_users(request: Request):
    return templates.TemplateResponse(request=request,name="all_users.html",context={"users":get_all_users()})

@router.post("/delete-user")
def delete_user_route(user_id:str=Form(...)):
    delete_user(user_id); return RedirectResponse(url="/view-all-users",status_code=303)
