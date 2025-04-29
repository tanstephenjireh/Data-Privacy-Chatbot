from fastapi import HTTPException, status

ChatDoesNotExistException: HTTPException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Chat does not exist."
)

MessageInvalidInputException: HTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Message Input"
)