from app import db

class BaseModel(db.Model):
    __abstract__ = True
    
    @property
    def get_columns(self):
        return [column.name for column in self.__table__.columns]
    
    def __getitem__(self, key):
        if key in self.get_columns:
            return getattr(self, key)
        raise KeyError(f"Invalid column name for column query: {key}")
    
    @classmethod
    def __class_getitem__(cls, key):
        """
        row_data = DB_MODEL_CLASS["COLUMN_NAME", "VALUE"]
        """
        if isinstance(key, tuple) and len(key) == 2:
            column, value = key
            return cls.get_row(column, value)
        raise KeyError("Invalid parameters, must be a tuple of (column, value)")
    
    
    # Row Methods
    
    ## Queries and returns instance where value = value in column.
    @classmethod
    def get_row(cls, column, value):
        """
        Returns first row where value is in the specified column.
        """
        if column not in [c.name for c in cls.__table__.columns]:
            raise KeyError(f"Invalid column name for row query: {column}")
        return cls.query.filter(getattr(cls, column) == value).first()
    
    ## Update on an instance
    def update_row(self, **kwargs):
        """
        Updates row instance, kwargs must match columns.
        """
        for key, value in kwargs.items():
            if key in self.get_columns:
                setattr(self, key, value)
            else:
                raise KeyError(f"Invalid column name: {key}")
        db.session.commit()
        
    @classmethod
    def add_row(cls, **kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance