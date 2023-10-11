#!/usr/bin/python3
"Database Engine"

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import user, user_profile, contribution, loan, loan_out, loan_profile, loan_refund, interest


class DB:
    """Handle Data Persistence in DBstorage"""

    MODELS = {
        'User': user.User,
        'UserProfile': user_profile.UserProfile,
        'Contribution': contribution.Contribution,
        'Loan': loan.Loan,
        'LoanOut': loan_out.LoanOut,
        'LoanProfile': loan_profile.LoanProfile,
        'LoanRefund': loan_refund.LoanRefund,
        'Interest': interest.Interest,
    }

    __engine = None
    __session = None

    def __init__(self) -> None:
        """Create the engine -- self.__engine"""
        if os.environ.get('ST_ENV') == 'DEV':
            self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                    os.environ.get('ST_USER'),
                    os.environ.get('ST_PWD'),
                    os.environ.get('ST_HOST'),
                    os.environ.get('ST_DB'),
                )
            )
        else:
            self.__engine = create_engine("sqlite:///std.db", echo=False)
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """create all tables in database & session from the engine"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            )
        )

    def shutdown_db(self):
        """Close current DB session"""
        self.__session.remove()

    def rollback(self):
        """Roll back current DB session"""
        self.__session.rollback()

    def all(self, cls=None) -> dict:
        """ returns a dictionary of all objects"""
        dict_obj = {}
        if cls is not None:
            try:
                query = self.__session.query(cls)
                for obj in query:
                    obj_ref = f'{type(obj).__name__}.{obj.id}'
                    dict_obj[obj_ref] = obj
                return dict_obj
            except Exception:
                raise ValueError('Incorrect Class Model Passed')

        for cls in DB.MODELS.values():
            query = self.__session.query(cls)
            for obj in query:
                obj_ref = f'{type(obj).__name__}.{obj.id}'
                dict_obj[obj_ref] = obj
        return dict_obj

    def get_by_attribute(self, cls, attribute_name, attribute_value):
        """Retrieve an object based on a class name and an attribute's value"""
        if cls and attribute_name and attribute_value:
            try:
                query = self.__session.query(cls).filter(
                    getattr(cls, attribute_name) == attribute_value)
                return query.first()
            except Exception:
                raise ValueError(
                    'Incorrect Class Model or Attribute Name Passed')

        return None

    def paginate(self, cls, page, page_size, search_column: str | None = None, search_query: str | None = None):
        """Custom Pagination + search params"""
        dict_obj = {}
        total_items = self.count(cls)
        total_pages = (total_items - 1) // page_size + 1
        page = (page - 1) * page_size

        if cls is not None:
            try:
                query = self.__session.query(
                    cls)

                # Apply search params if any
                if search_column and search_query:
                    search_column = getattr(cls, search_column)
                    query = query.filter(
                        search_column.like(f"%{search_query}%"))
                    # Reset Total items if a search is passed
                    total_items = len(query.all())
                    total_pages = (total_items - 1) // page_size + 1

                query = query.limit(page_size).offset(page).all()
                for obj in query:
                    obj_ref = f'{type(obj).__name__}.{obj.id}'
                    dict_obj[obj_ref] = obj
                return dict_obj, total_pages, total_items
            except Exception:
                raise ValueError('Incorrect Class Model Passed')

    def new(self, obj):
        """add objects to current database session"""
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session"""
        self.__session.commit()

    def get(self, cls, id: str):
        """retrieves one object based on a class name and id"""
        if cls and id:
            dict_key = f'{cls.__name__}.{id}'
            all_obj = self.all(cls)
            return all_obj.get(dict_key)
        return None

    def get_by_email(self, email: str) -> user.User:
        """retrieve a user by their email"""
        if email:
            db_user = self.__session.query(DB.MODELS['User']).filter(
                user.User.email == email).first()
            return db_user
        return None

    def delete(self, obj=None):
        """Delete an object from the current database session if not None"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def count(self, cls=None) -> int:
        """Return the count of all objects in storage"""
        return (len(self.all(cls)))
