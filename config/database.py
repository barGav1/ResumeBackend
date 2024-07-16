from motor.motor_asyncio import AsyncIOMotorClient

# Create an asynchronous MongoDB client
client = AsyncIOMotorClient("mongodb+srv://admin:1234@cluster0.yyfuwwb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Access the database
db = client.todo_db

# Access the collections
db_resumes = db["resumes_collection"]
db_users = db["users_collection"]
