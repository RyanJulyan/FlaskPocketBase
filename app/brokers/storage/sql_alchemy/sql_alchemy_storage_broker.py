from dataclasses import dataclass

from app import app, db
from app.brokers.storage.i_storage_broker import IStorageBroker


@dataclass
class SQLAlchemyStorageBroker(IStorageBroker):

    def create(self, data, *args, **kwargs):
        db.session.add(data)
        db.session.commit()

        return data

    def read_single(self, query, *args, **kwargs):
        data = query.first_or_404()

        return data

    def read_all(self, query, page, *args, **kwargs):
        data = query.paginate(page=page, per_page=app.config["ROWS_PER_PAGE"]).items

        return data

    def update(self, *args, **kwargs):
        db.session.commit()

    def delete(self, query, id, *args, **kwargs):
        data = self.get_or_404(query=query, id=id)

        db.session.delete(data)
        db.session.commit()

        return data

    def get_or_404(self, query, id):
        data = query.get_or_404(id)

        return data
