#!/usr/bin/python3
"Database Engine"

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import user, user_profile, contribution, loan, loan_profile, loan_refund, interest


class DB:
    """Handle Data Persistence in DBstorage"""

    MODELS = {
        'User': user.User,
        'UserProfile': user_profile.UserProfile,
        'Contribution': contribution.Contribution,
        'Loan': loan.Loan,
        'LoanProfile': loan_profile.LoanProfile,
        'LoanRefund': loan_refund.LoanRefund,
        'Interest': interest.Interest
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
            # Base.metadata.drop_all(self.__engine)

    def reload(self):
        """create all tables in database & session from the engine"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            )
        )

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
