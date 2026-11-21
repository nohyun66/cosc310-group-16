from fastapi import HTTPException

def fail(status, msg):
    raise HTTPException(status_code=status, detail=msg)