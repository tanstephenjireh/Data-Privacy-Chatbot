from fastapi import HTTPException, status

InvalidCredentialsException: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)

NotAuthorizedException: HTTPException = HTTPException (
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authorized.",
)

NotAuthenticatedException: HTTPException = HTTPException (
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated.",
    headers={"WWW-Authenticate": "Bearer"},
)

UserExistsException: HTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username or email already exists.",
)

UserDoesNotExistException: HTTPException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist."
)