from fastapi import APIRouter, Depends, HTTPException, status
from open_webui.models.sidebar_links import SidebarLinks, SidebarLinkForm, SidebarLinkModel
from open_webui.utils.auth import get_admin_user, get_verified_user

router = APIRouter()


@router.get("/", response_model=list[SidebarLinkModel])
async def get_sidebar_links(user=Depends(get_verified_user)):
    return SidebarLinks.get_links()


@router.post("/create", response_model=SidebarLinkModel)
async def create_sidebar_link(form: SidebarLinkForm, user=Depends(get_admin_user)):
    return SidebarLinks.insert_link(form)


@router.post("/{link_id}/update", response_model=SidebarLinkModel)
async def update_sidebar_link(link_id: str, form: SidebarLinkForm, user=Depends(get_admin_user)):
    link = SidebarLinks.update_link(link_id, form)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@router.delete("/{link_id}", response_model=bool)
async def delete_sidebar_link(link_id: str, user=Depends(get_admin_user)):
    result = SidebarLinks.delete_link(link_id)
    if not result:
        raise HTTPException(status_code=404, detail="Link not found")
    return True
