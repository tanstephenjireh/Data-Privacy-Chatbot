from functools import wraps
from datetime import datetime
from app.utilities.spiels import FAILURE_SPIEL
from app.repositories import telemetry as telemetry_repo
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.repositories import messages as message_repo
from app.schemas.messages import MessageModified

def log_timing(func):
    """Decorator for logging OpenAI Call Latency"""
    
    @wraps(func)
    async def persist_log(*args, **kwargs):
        log_map = {}
        log_map["endpoint"] = "/messages"
        log_map["input"] = str(kwargs["message_input"].dict())

        time_start = datetime.now()
        log_map["start_time"] = time_start

        try:
            result = await func(*args, **kwargs)
            output = f"message id: {result['id']}"
        except Exception as e:
            message = ""
            error_class = "None"
            
            if hasattr(e, 'message'):
                message = e.message
            else:
                message = str(e)
            
            if message == "":
                message = "None"

            if hasattr(e, '__class__'):
                error_class = e.__class__
            
            error_message = f"Class: {error_class}\nMessage: {message}"
            log_map["status"] = "ERROR: 500"
            log_map["response"] = error_message
            time_end = datetime.now()
            log_map["end_time"] = time_end

            await telemetry_repo.create(log_map)

            raise e
        
        time_end = datetime.now()
        log_map["end_time"] = time_end
        log_map["status"] = "SUCCESS: 200"
        log_map["response"] = output
        

        await telemetry_repo.create(log_map)

        return result
    
    return persist_log

def failover(func):
    """Decorator for handling any failure mode on the /messages api"""
    
    @wraps(func)
    async def failover_wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            chat_id = int(kwargs["message_input"].chat_id)
            return await track_failed_messages(chat_id=chat_id, message=FAILURE_SPIEL)
        
        return result
    
    return failover_wrapper

async def track_failed_messages(chat_id, message):
    failed_reply = MessageModified(
        chat_id=chat_id,
        user_id=None,
        message=message,
        modified_message=message,
        type="ai",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_liked=0,
        is_disliked=0,
    )

    return await message_repo.create(failed_reply) 

def remove_failed_messages(conversation_history):
    filtered_coversation_history = []
    for record in conversation_history:
        if record.message == FAILURE_SPIEL: # Don't include failed messages
            if len(filtered_coversation_history) != 0 and filtered_coversation_history[-1].type == "human": # Remove previous messages if their response was failed
                filtered_coversation_history.pop()
            continue
        filtered_coversation_history.append(record)
        
    
    return filtered_coversation_history



