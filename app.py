from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

app = FastAPI()


class MaintenanceRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    equipment_name: str
    description: str
    priority: str
    status: str
    technician: str
    department: str


class MaintenanceRecordUpdate(BaseModel):
    equipment_name: str | None = None
    description: str | None = None
    priority: str | None = None
    status: str | None = None
    technician: str | None = None
    department: str | None = None


records: dict[UUID, MaintenanceRecord] = {}


@app.post("/records")
def create_record(record_data: MaintenanceRecord):
    record_id = record_data.id
    records[record_id] = record_data
    return JSONResponse(record_data.model_dump(mode="json"), status_code=201)


@app.get("/records")
def get_all_records():
    return list(records.values())


@app.get("/records/{record_id}")
def get_record_by_id(record_id: UUID):
    exists = record_id in records
    
    if not exists:
        raise HTTPException(detail=f"Record with id: {str(record_id)} not found", status_code=404)
    
    return records[record_id]


@app.put("/records/{record_id}")
def full_update_record(record_id: UUID, record_data: MaintenanceRecord):
    exists = record_id in records
    
    record_data.id = record_id
    record_data.updated_at = datetime.now()
    
    if not exists:
        record_data.created_at = datetime.now()
        records[record_id] = record_data
        
        return JSONResponse(record_data.model_dump(mode="json"), status_code=201)
    
    else:
        record_data.created_at = records[record_id].created_at
        records[record_id] = record_data
        return record_data


@app.patch("/records/{record_id}")
def partial_update_record(record_id: UUID, partial_record_data: MaintenanceRecordUpdate):
    exists = record_id in records
    
    if not exists:
        raise HTTPException(detail=f"Record with id: {str(record_id)} not found", status_code=404)
    
    existing_record = records[record_id]
    
    update_data = partial_record_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing_record, field, value)
    
    existing_record.updated_at = datetime.now()
    
    records[record_id] = existing_record
    
    return existing_record


@app.delete("/records/{record_id}")
def delete_record(record_id: UUID):
    exists = record_id in records
    
    if not exists:
        raise HTTPException(detail=f"Record with id: {str(record_id)} not found", status_code=404)
    
    del records[record_id]
    return Response(status_code=204)
