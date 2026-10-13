from fastapi import FastAPI, HTTPException

app = FastAPI()

# Простая «база» в памяти: {id: {"name": ..., "age": ..., "sex": ...}}
users_db = {}
next_id = 1

@app.get("/")
def read_root():
    return {"message": "Hello, API is working!"}

@app.post("/v1/user")
def create_user(name: str, age: int, sex: str):
    global next_id
    user_id = next_id
    next_id += 1
    users_db[user_id] = {"name": name, "age": age, "sex": sex}
    return {
        "id": user_id,
        "name": name,
        "age": age,
        "sex": sex
    }

@app.put("/v1/user/{user_id}")
def update_user(user_id: int, name: str, age: int, sex: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = {"name": name, "age": age, "sex": sex}
    return {
        "id": user_id,
        **users_db[user_id]
    }

@app.delete("/v1/user/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    deleted = users_db.pop(user_id)
    return {
        "message": "User deleted",
        "deleted": deleted
    }
