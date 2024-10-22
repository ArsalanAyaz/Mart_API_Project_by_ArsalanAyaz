from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from requests import get,post
from typing import Annotated,Any,Dict
from fastapi import Depends, HTTPException, status




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: Annotated[str | None, Depends(oauth2_scheme)]):
    # print(f"Token: {token}")

    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    url = f"http://user-service-api:8005/user_profile"
    headers = {"Authorization": f"Bearer {token}"}

    response = get(url, headers=headers)

    # print( "AUTHENTICATED_USER_DATA" ,response.json())

    if response.status_code == 200:
        user_data = response.json()
        return user_data
    
    raise HTTPException(status_code=response.status_code, detail=f"{response.text}")
    

GetCurrentUserDep = Annotated[Dict[str, Any], Depends(get_current_user)]  # Type hinting for a dictionary

def get_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    url = f"http://user-service-api:8005/token"
    data = {
        "username":form_data.username,
        "password":form_data.password
    }
    response = post(url,data=data)
    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=response.status_code,detail=f"{response.text}")

LoginForAccessTokenDep = Annotated[dict, Depends(get_login_for_access_token)]



def admin_required(current_user: Annotated[Dict[str, Any], Depends(get_current_user)]):
    print("Current User Data:", current_user)  # Add this line
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user