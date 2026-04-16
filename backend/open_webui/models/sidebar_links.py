import time
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, Integer, String, Text
from open_webui.internal.db import Base, get_db


class SidebarLink(Base):
    __tablename__ = "sidebar_link"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    icon = Column(String, nullable=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(BigInteger, default=lambda: int(time.time()))


class SidebarLinkModel(BaseModel):
    id: str
    title: str
    url: str
    icon: Optional[str] = None
    sort_order: int = 0
    created_at: int

    model_config = ConfigDict(from_attributes=True)


class SidebarLinkForm(BaseModel):
    title: str
    url: str
    icon: Optional[str] = None
    sort_order: Optional[int] = 0


class SidebarLinksTable:
    def insert_link(self, form: SidebarLinkForm) -> Optional[SidebarLinkModel]:
        with get_db() as db:
            link = SidebarLink(
                id=str(uuid.uuid4()),
                title=form.title,
                url=form.url,
                icon=form.icon,
                sort_order=form.sort_order or 0,
                created_at=int(time.time()),
            )
            db.add(link)
            db.commit()
            db.refresh(link)
            return SidebarLinkModel.model_validate(link)

    def get_links(self) -> list[SidebarLinkModel]:
        with get_db() as db:
            links = db.query(SidebarLink).order_by(SidebarLink.sort_order.asc()).all()
            return [SidebarLinkModel.model_validate(l) for l in links]

    def update_link(self, id: str, form: SidebarLinkForm) -> Optional[SidebarLinkModel]:
        with get_db() as db:
            link = db.query(SidebarLink).filter_by(id=id).first()
            if not link:
                return None
            link.title = form.title
            link.url = form.url
            link.icon = form.icon
            link.sort_order = form.sort_order or 0
            db.commit()
            db.refresh(link)
            return SidebarLinkModel.model_validate(link)

    def delete_link(self, id: str) -> bool:
        with get_db() as db:
            link = db.query(SidebarLink).filter_by(id=id).first()
            if not link:
                return False
            db.delete(link)
            db.commit()
            return True


SidebarLinks = SidebarLinksTable()
