from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .models import Contact
from .schemas import ContactCreate, ContactUpdate

async def get_contact(db: AsyncSession, contact_id: int) -> Optional[Contact]:
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    return result.scalars().first()

async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Contact]:
    result = await db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()

async def create_contact(db: AsyncSession, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def update_contact(db: AsyncSession, contact_id: int, contact: ContactUpdate) -> Optional[Contact]:
    db_contact = await get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        await db.commit()
        await db.refresh(db_contact)
        return db_contact
    return None

async def delete_contact(db: AsyncSession, contact_id: int) -> bool:
    db_contact = await get_contact(db, contact_id)
    if db_contact:
        await db.delete(db_contact)
        await db.commit()
        return True
    return False

async def search_contacts(db: AsyncSession, query: str) -> List[Contact]:
    result = await db.execute(
        select(Contact).where(
            (Contact.first_name.ilike(f"%{query}%")) |
            (Contact.last_name.ilike(f"%{query}%")) |
            (Contact.email.ilike(f"%{query}%"))
        )
    )
    return result.scalars().all()

async def get_upcoming_birthdays(db: AsyncSession) -> List[Contact]:
    from datetime import datetime, timedelta
    today = datetime.today().date()
    upcoming_date = today + timedelta(days=7)
    result = await db.execute(
        select(Contact).where(
            Contact.birthday.between(today, upcoming_date)
        )
    )
    return result.scalars().all()
