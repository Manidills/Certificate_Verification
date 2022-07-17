from sqlalchemy import Column, Integer, Table, create_engine, Text, Date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import func

DB_URL = "sqlite:///test.db"
Base = declarative_base()


def create_db():
    engine = create_engine(DB_URL)


class TableModel(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)  # Unique id auto increment
    name = Column(Text, nullable=False)
    ipfs_hash = Column(Text, nullable=False)
    block_chain_hash = Column(Text, nullable=False)
    record_date = Column(Date, default=func.current_date())


class TableDba:
    def __init__(self, model=TableModel):
        self.model = model
        engine = create_engine(DB_URL, poolclass=NullPool)
        self.session = sessionmaker()
        self.session.configure(bind=engine)
        Base.metadata.create_all(engine)

    def get(self, name, record_date):
        s = self.session()
        result = {'data': []}
        try:
            q = s.query(TableModel).filter_by(name=name).filter_by(record_date=record_date).all()
            print('query', q)
            for r in q:
                res = {'id': r.id,
                       'name': r.name,
                       'ipfs_hash': r.ipfs_hash,
                       'block_chain_hash': r.block_chain_hash,
                       'date': r.record_date
                       }
                result['data'].append(res)
        except SQLAlchemyError as e:
            s.rollback()
            print('{cls}: DB Error: {err}'.format(cls=self.__class__.__name__, err=str(e)))
        except Exception as e:
            s.rollback()
            print('{cls}: DB Error: {err}'.format(cls=self.__class__.__name__, err=str(e)))
        finally:
            s.close()
            return result

    def add_entry(self, entry):
        s = self.session()
        try:
            s.add(self.model)
            s.commit()
            s.refresh(entry)
            return True

        except Exception as e:
            print('got error while adding entry', e)
        except SQLAlchemyError as e1:
            print('got error while adding entry', e1)
        finally:
            s.close()

    def delete_all(self):
        s = self.session()
        try:
            q = s.query(TableModel).delete()
            s.commit()
            return q
        except SQLAlchemyError as err:
            s.rollback()
            print('got error while deleting all date',str(err))
            return err
        finally:
            s.close()
