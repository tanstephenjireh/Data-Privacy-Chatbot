from app.database import database
from app.models.telemetry import telemetry

async def create(telemetry_input: dict):
    query = telemetry.insert()
    values = telemetry_input

    id = await database.execute(query=query, values=values)

    return {"id": id, "entries": telemetry_input}
