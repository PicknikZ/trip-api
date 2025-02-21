from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class TripBase(BaseModel):
    title: str = Field(..., description="旅程名称")
    start_date: date = Field(..., description="开始日期")
    duration: int = Field(..., description="持续天数", gt=0)
    cities: List[dict] = Field(..., description="城市数组（名称+顺序+到达时间）")
    style_tags: List[str] = Field(..., description="旅行风格标签数组")
    settings: dict = Field(..., description="交通优先级等配置")

class TripCreate(TripBase):
    owner_id: Optional[str] = Field(None, description="创建者ID")

class TripResponse(TripBase):
    id: int = Field(..., description="旅程ID")
    is_pinned: bool = Field(False, description="是否置顶")
    created_at: date = Field(..., description="创建时间")

    class Config:
        orm_mode = True

class FavoriteRequest(BaseModel):
    trip_id: str = Field(..., description="旅程ID")