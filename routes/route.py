from fastapi import APIRouter, HTTPException, Response, Request,status
from pydantic import ValidationError
from bson import ObjectId
from  models.users import User
from  models.resumes import Resume
import uuid
from config.database import db_resumes, db_users 
from schema.schemas import list_users

router = APIRouter()

def object_id_to_str(obj_id: ObjectId) -> str:
    return str(obj_id)

def str_to_object_id(str_id: str) -> ObjectId:
    return ObjectId(str_id)

# Function to get user by email
async def get_user_by_email(email: str):
    user = await db_users.find_one({"email": email})
    return user

# Authentication Routes
@router.post("/login/")
async def login_user(user: User, response: Response):
    # Debugging output
    print(f"Attempting login for email: {user.email}")

    # Fetch user from the database
    existing_user = await get_user_by_email(user.email)
    if not existing_user:
        print("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify the password (ensure you are comparing hashed passwords if applicable)
    if existing_user.get("password") != user.password:
        print("Invalid credentials")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create session and set cookies
    session_id = str(uuid.uuid4())
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    response.set_cookie(key="user_id", value=str(existing_user["_id"]), httponly=True)

    return {
        "message": "Login successful",
        "user": {
            "id": str(existing_user["_id"]),
            "email": existing_user["email"]
        }
    }

@router.post("/logout/")
async def logout_user(response: Response, request: Request):
    response.delete_cookie("session_id")
    response.delete_cookie("user_id")
    return {"message": "Logged out"}

@router.post("/users/")
async def post_user(user: User):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    db_users.insert_one(dict(user))
    return {"message": "User Created"}

@router.get("/users/")
async def get_users():
    try:
        cursor = db_users.find()
        users = await cursor.to_list(length=100)  # Adjust length as needed or remove if you want all documents
        return list_users(users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    try:
        user_object_id = ObjectId(user_id)
        user = await db_users.find_one({"_id": user_object_id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        # Convert ObjectId to string if necessary
        user['id'] = object_id_to_str(user['_id'])
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resumes/", response_model=Resume)
async def create_resume(resume: Resume):
    try:
        if not resume.user_id:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User ID is required")
        # Check for the first available resume number (up to 4)
        for resume_number in range(1, 5):
            existing_resume = await db_resumes.find_one({"user_id": resume.user_id, "resume_number": resume_number})
            if not existing_resume:
                resume.resume_number = resume_number
                resume_dict = resume.dict()
                resume_dict["_id"] = ObjectId()
                await db_resumes.insert_one(resume_dict)
                return resume_dict
        
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="All 4 resume slots are occupied")

    except ValidationError as e:
        # This will catch Pydantic validation errors and return them in detail
        error_messages = []
        for error in e.errors():
            error_messages.append({
                "loc": " -> ".join(map(str, error["loc"])),
                "msg": error["msg"],
                "type": error["type"]
            })
        if (error_messages):
            print("why are you doing this")
            raise HTTPException(status_code=422, detail=error_messages)
    
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}/resumes/{resume_number}", response_model=Resume)
async def get_resume(user_id: str, resume_number: int):
    resume = await db_resumes.find_one({"user_id": user_id, "resume_number": resume_number})
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume["id"] = object_id_to_str(resume["_id"])
    return resume

@router.put("/users/{user_id}/resumes/{resume_number}", response_model=Resume)
async def update_resume(user_id: str, resume_number: int, resume: Resume):
    existing_resume = await db_resumes.find_one({"user_id": user_id, "resume_number": resume_number})
    if existing_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    updated_resume = await db_resumes.update_one({"user_id": user_id, "resume_number": resume_number}, {"$set": resume.dict()})
    if updated_resume.modified_count == 1:
        updated_resume = await db_resumes.find_one({"user_id": user_id, "resume_number": resume_number})
        updated_resume["id"] = object_id_to_str(updated_resume["_id"])
        return updated_resume
    
    raise HTTPException(status_code=400, detail="Resume update failed")

@router.delete("/users/{user_id}/resumes/{resume_number}")
async def delete_resume(user_id: str, resume_number: int):
    result = await db_resumes.delete_one({"user_id": user_id, "resume_number": resume_number})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume deleted successfully"}