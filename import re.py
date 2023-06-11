import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PasswordRequest(BaseModel):
    password: str

def validate_password(password):
    if len(password) < 12:
        return False
    if not re.search(r'[@#$%&*()_+=<>?;:.]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

passwords = []

@app.post("/check_password")
def check_password_strength(password_req: PasswordRequest):
    password = password_req.password
    if validate_password(password):
        passwords.append(password)
        return {"message": "密碼符合要求並已儲存。"}
    else:
        raise HTTPException(status_code=400, detail="密碼不符合要求")

@app.get("/passwords")
def get_passwords():
    return {"passwords": passwords}

@app.put("/passwords/{index}")
def update_password(index: int, password_req: PasswordRequest):
    password = password_req.password
    if index >= 0 and index < len(passwords):
        if validate_password(password):
            passwords[index] = password
            return {"message": "密碼已成功更新。"}
        else:
            raise HTTPException(status_code=400, detail="新密碼不符合要求")
    else:
        raise HTTPException(status_code=404, detail="找不到該密碼")

@app.delete("/passwords/{index}")
def delete_password(index: int):
    if index >= 0 and index < len(passwords):
        passwords.pop(index)
        return {"message": "密碼已成功刪除。"}
    else:
        raise HTTPException(status_code=404, detail="找不到該密碼")