from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Any, List, Optional, Generic, TypeVar
from pydantic import BaseModel, ConfigDict
from pydantic.generics import GenericModel

# 泛型支持
T = TypeVar("T")

class PageQuery(BaseModel):
    """通用分页请求基类（最佳实践方案）"""
    current: int = 1 
    page_size: int = 10
    # 若需要OpenAPI规范示例值，可添加注解：
    model_config = ConfigDict(json_schema_extra={"example": {"current": 1, "page_size": 10}})


class Pagination(BaseModel):
    current_page: int
    page_size: int
    total: int
    total_pages: int  # 总页数

    @classmethod
    def create(cls, current_page: int, page_size: int, total: int):
        return cls(
            current_page=current_page,
            page_size=page_size,
            total=total,
            total_pages=(total + page_size - 1)
        )

class BaseResponse(GenericModel, Generic[T]):
    code: int
    msg: str = ""
    data: Optional[T] = None
    error: Optional[str] = None
    pagination: Optional[Pagination] = None

class CommonResponse:
    @staticmethod
    def success(
        data: Any = None,
        msg: str = "success",
        **kwargs
    ) -> JSONResponse:
        """
        通用成功响应
        示例: /api/users/1
        """
        content = {
            "code": 0,
            "msg": msg,
            "data": jsonable_encoder(data)
        }
        content.update(kwargs)
        return JSONResponse(
            status_code=200,
            content=content,
            media_type="application/json"
        )

    @staticmethod
    def failed(
        err_msg: str,
        **kwargs
    ) -> JSONResponse:
        """
        通用失败响应
        示例: 参数校验失败
        """
        content = {
            "code": 0,
            "error": err_msg
        }
        content.update(kwargs)
        return JSONResponse(
            status_code=200,
            content=content,
            media_type="application/json"
        )
    
    @staticmethod
    def failed(
        status_code: int,
        err_msg: str,
        **kwargs
    ) -> JSONResponse:
        """
        通用失败响应
        示例: 参数校验失败
        """
        content = {
            "code": status_code,
            "error": err_msg
        }
        content.update(kwargs)
        return JSONResponse(
            status_code=status_code,
            content=content,
            media_type="application/json"
        )

    @staticmethod
    def table_success(
        data: List[Any],
        pagination: Pagination,
        msg: str = "success",
        **kwargs
    ) -> JSONResponse:
        """
        表格数据成功响应
        示例: /api/users?page=1
        """
        content = {
            "code": 0,
            "msg": msg,
            "list": jsonable_encoder(data),
            "pagination": pagination.dict()
        }
        content.update(kwargs)
        return JSONResponse(
            status_code=200,
            content=content,
            media_type="application/json"
        )

    @staticmethod
    def table_success(
        data: List[Any],
        page: PageQuery,
        total: int,
        msg: str = "success",
        **kwargs
    ) -> JSONResponse:
        """
        表格数据成功响应
        示例: /api/users?page=1
        """
        content = {
            "code": 0,
            "msg": msg,
            "list": data,
            "pagination": Pagination.create(page.current, page.page_size, total)
        }
        content.update(kwargs)
        return JSONResponse(
            status_code=200,
            content=content,
            media_type="application/json"
        )

    @staticmethod
    def table_success(
        data: List[Any],
        current: int,
        page_size: int,
        total: int,
        msg: str = "success",
        **kwargs
    ) -> JSONResponse:
        """
        表格数据成功响应
        示例: /api/users?page=1
        """
        content = {
            "code": 0,
            "msg": msg,
            "list": jsonable_encoder(data),
            "pagination": Pagination.create(current, page_size, total)
        }
        content.update(kwargs)
        return JSONResponse(
            status_code=200,
            content=content,
            media_type="application/json"
        )


    @staticmethod
    def table_failed(
        err_msg: str,
        pagination: Optional[Pagination] = None,
        **kwargs
    ) -> JSONResponse:
        """
        表格数据失败响应
        示例: 分页参数错误
        """
        content = {
            "code": 0,
            "error": err_msg,
            "pagination": pagination.dict() if pagination else None
        }
        content.update(kwargs)
        return JSONResponse(
            status_code=200,
            content=content,
            media_type="application/json"
        )