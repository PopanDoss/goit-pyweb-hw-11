from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List

from datetime import date

from shemas import ContactAdd, ContactUpdate, ContactBase
from database.db import get_db
from repository.contacts_crud import search_contact, add_contact, update_contact, del_contact, all_contacts, search_born_date, search_born_date_7days

router = APIRouter()


@router.post("/contacts/", response_model=ContactBase)
def new_add_contact(contact: ContactAdd, db: Session = Depends(get_db)):

    db_contact = search_contact(db, contact_email=contact.email)

    if db_contact:

        raise HTTPException(status_code=400, detail="Email already registered")
    
    return add_contact(db=db, contact=contact)


@router.get("/contacts/", response_model=List[ContactBase])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    contacts = all_contacts(db, skip=skip, limit=limit)
    
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactBase)
def read_contact_id(contact_id: int,  db: Session = Depends(get_db)):

    db_contact = search_contact(db, contact_id=contact_id)

    if db_contact is None:

        raise HTTPException(status_code=404, detail="Contact not found")
    
    return db_contact


@router.get("/contacts/search/", response_model=ContactBase)
def read_contact_search(firstname: str = None, lastname: str = None , email: str = None, db: Session = Depends(get_db)):

    if firstname:
        db_contact = search_contact(db, contact_firstname=firstname)
    
    elif lastname:
        db_contact = search_contact(db, contact_lastname=lastname)
    
    elif email:
        db_contact = search_contact(db, contact_email=email)

    else:

        raise HTTPException(status_code=404, detail="Contact not found")
    
    return db_contact


@router.put("/contacts/{contact_id}", response_model=ContactBase)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):

    db_contact = search_contact(db, contact_id=contact_id)

    if db_contact is None:

        raise HTTPException(status_code=404, detail="Contact not found")
    
    return update_contact(db=db, contact_id=contact_id, contact=contact)


@router.delete("/contacts/{contact_id}", response_model=ContactBase)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):

    db_contact = search_contact(db, contact_id=contact_id)

    if db_contact is None:

        raise HTTPException(status_code=404, detail="Contact not found")
    
    return del_contact(db=db, contact_id=contact_id)


@router.get("/contacts/contact_born_dates/", response_model=List[ContactBase])
def read_contacts_born_date(contacts_born_date: date,  db: Session = Depends(get_db)):

    contacts = search_born_date(db, born_date=contacts_born_date)

    return contacts


@router.get("/contacts/borndate_next_7days/", response_model=List[ContactBase])
def read_contacts_7days(db: Session = Depends(get_db)):

    contacts = search_born_date_7days(db)
    
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found with birthdays in the next 7 days")
    return contacts