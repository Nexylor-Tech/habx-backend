from typing import Optional

from bson.objectid import ObjectId
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import settings
from app.db import user_collection, workspace_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(
#             token,
#             settings.SECRET_KEY.get_secret_value(),
#             algorithms=[settings.ALGORITHM],
#         )
#         email: str = payload.get("sub")
#         if email is None:
#             raise credential_exception
#     except JWTError:
#         raise credential_exception
#
#     user = await user_collection.find_one({"email": email})
#     if user is None:
#         raise credential_exception
#     return user


# TODO:Clerk Auth Implementatio
async def get_current_user(creds: dict):
    token = creds["credentials"]
    try:
        claims = jwt.decode(token, settings.CLERK_PEM_PUBLIC_KEY, algorithms=[settings.ALGORITHM], options={"verify_aud": False})
        clerk_id = claims.get("sub")
        email = claims.get("email")

        if not clerk_id:
            raise HTTPException(status_code=401, detail="Invalid Token")
        user = await user_collection.find_one({"clerk_id": clerk_id})
        return {"clerk_id": clerk_id, "user": user, "token_email": email}
    except:
        raise HTTPException(status_code=401, detail="Invalid Auth Creds")


async def get_current_workspace_id(
    x_workspace_id: Optional[str] = Header(None),
    current_user: dict = Depends(get_current_user),
) -> str:
    if x_workspace_id:
        if not ObjectId.is_valid(x_workspace_id):
            raise HTTPException(status_code=400, detail="Invalid Workspace")

        workspace = await workspace_collection.find_one(
            {"_id": ObjectId(x_workspace_id), "user_id": current_user["_id"]}
        )

        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")

        return x_workspace_id

    workspace = await workspace_collection.find_one({"user_id": current_user["_id"]})
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return str(workspace["_id"])
