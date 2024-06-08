from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud, models, schemas
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Contact)
async def create_contact(contact: schemas.ContactCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_contact(db, contact)

@router.get("/", response_model=List[schemas.Contact])
async def read_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_contacts(db, skip=skip, limit=limit)

@router.get("/{contact_id}", response_model=schemas.Contact)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=schemas.Contact)
async def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=bool)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_contact(db, contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return success

@router.get("/search/", response_model=List[schemas.Contact])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    return await crud.search_contacts(db, query)

@router.get("/birthdays/", response_model=List[schemas.Contact])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    return await crud.get_upcoming_birthdays(db)
