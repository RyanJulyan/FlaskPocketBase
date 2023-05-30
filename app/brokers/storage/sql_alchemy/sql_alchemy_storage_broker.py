from dataclasses import dataclass
from typing import Any, Callable, Dict, Literal

from app import app, db
from app.brokers.storage.i_storage_broker import IStorageBroker


@dataclass
class SQLAlchemyStorageBroker(IStorageBroker):
    def create(self, data: Any, *args: Any, **kwargs: Any) -> Any:
        db.session.add(data)
        db.session.commit()

        return data

    def read(
        self, read_type: Literal["single", "all"], *args: Any, **kwargs: Any
    ) -> Any:
        read_type_factory: Dict[str, Callable[..., Any]] = {
            "single": self.read_single,
            "all": self.read_all,
        }

        return read_type_factory[read_type](*args, **kwargs)

    def read_single(self, query: Any, *args: Any, **kwargs: Any) -> Any:
        data = query.first_or_404()

        return data

    def read_all(
        self, query: Any, page: int, *args: Any, **kwargs: Any
    ) -> Any:
        data = query.paginate(
            page=page, per_page=app.config["ROWS_PER_PAGE"]
        ).items

        return data

    def update(self, *args: Any, **kwargs: Any) -> Any:
        db.session.commit()

    def delete(self, query: Any, id: int, *args: Any, **kwargs: Any) -> Any:
        data = self.get_or_404(query=query, id=id)

        db.session.delete(data)
        db.session.commit()

        return data

    def get_or_404(self, query: Any, id: int) -> Any:
        data = query.get_or_404(id)

        return data
