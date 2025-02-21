from typing import Any, Dict, Optional, Sequence, Type
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from starlette.status import *


class MysqlException(SQLAlchemyError):
    def __init__(self, table_name: str, action: str, details: str):
        self.table_name = table_name
        self.action = action
        self.details = details

class ServerException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        comment: Any = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.comment = comment