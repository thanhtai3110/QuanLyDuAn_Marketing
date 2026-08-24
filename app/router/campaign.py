from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List, Optional

from app.models.campaign import Campaign, CampaignMember
from app.models.user import User
from app.schemas.campaign import CampaignUpdate
from app.schemas.campaign import CampaignMemberAdd, CampaignMemberResponse
from app.schemas.campaign import CampaignCreate, CampaignResponse

from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"]
)


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API Tạo chiến dịch:
    - Bắt buộc đăng nhập.
    - User tạo chiến dịch sẽ tự động trở thành OWNER.
    """

    # 1. Lưu thông tin chiến dịch vào DB
    new_campaign = Campaign(
        name=campaign_data.name,
        description=campaign_data.description,
        owner_id=current_user.id
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    # 2. Tự động cấp quyền OWNER trong bảng trung gian (CampaignMember)
    new_member = CampaignMember(
        campaign_id=new_campaign.id,
        user_id=current_user.id,
        role="OWNER"
    )

    db.add(new_member)
    db.commit()

    return new_campaign


@router.get("/", response_model=List[CampaignResponse], status_code=status.HTTP_200_OK)
def get_campaigns(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API Lấy danh sách chiến dịch:
    - Chỉ lấy những chiến dịch mà current_user có tham gia.
    - Có hỗ trợ tìm kiếm theo tên chiến dịch.
    """

    # Bước 1: Tìm tất cả Campaign mà User này có mặt trong bảng trung gian
    query = db.query(Campaign).join(CampaignMember).filter(
        CampaignMember.user_id == current_user.id
    )

    # Bước 2: Search
    if search:
        query = query.filter(
            Campaign.name.ilike(f"%{search}%")
        )

    # Bước 3: Lấy kết quả
    campaigns = query.all()

    return campaigns


@router.get("/{campaign_id}", response_model=CampaignResponse, status_code=status.HTTP_200_OK)
def get_campaign_detail(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API Lấy chi tiết chiến dịch:
    - Tìm chiến dịch theo ID.
    - Chỉ thành viên mới được xem.
    """

    # Tìm chiến dịch
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch này!"
        )

    # Kiểm tra thành viên
    is_member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem chiến dịch này!"
        )

    return campaign


# API 1: CẬP NHẬT CHIẾN DỊCH (Chỉ OWNER)

@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    campaign_data: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Bước 1: Tìm chiến dịch
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch!"
        )

    # Bước 2: Kiểm tra OWNER
    member_info = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if not member_info or member_info.role != "OWNER":
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền! Chỉ OWNER mới được phép sửa."
        )

    # Bước 3: Cập nhật dữ liệu
    if campaign_data.name is not None:
        campaign.name = campaign_data.name

    if campaign_data.description is not None:
        campaign.description = campaign_data.description

    db.commit()
    db.refresh(campaign)

    return campaign

# API 2: XÓA CHIẾN DỊCH (Chỉ OWNER)

@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Bước 1: Tìm chiến dịch
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch!"
        )

    # Bước 2: Kiểm tra OWNER
    member_info = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if not member_info or member_info.role != "OWNER":
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền! Chỉ OWNER mới được phép xóa."
        )

    # Bước 3: Xóa

    # Xóa toàn bộ member của campaign
    db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id
    ).delete()

    db.delete(campaign)

    db.commit()
    return

# API 3: THÊM THÀNH VIÊN (Chỉ OWNER)

@router.post("/{campaign_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(
    campaign_id: int,
    member_data: CampaignMemberAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Bước 1: Kiểm tra OWNER
    is_owner = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id,
        CampaignMember.role == "OWNER"
    ).first()

    if not is_owner:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền! Chỉ OWNER mới được thêm thành viên."
        )

    # Bước 2: Kiểm tra user
    user_to_add = db.query(User).filter(
        User.id == member_data.user_id
    ).first()

    if not user_to_add:
        raise HTTPException(
            status_code=404,
            detail="Người dùng này không tồn tại!"
        )

    # Bước 3: Chống thêm trùng
    existing_member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == member_data.user_id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="Người này đã là thành viên!"
        )

    # Bước 4: Thêm MEMBER
    new_member = CampaignMember(
        campaign_id=campaign_id,
        user_id=member_data.user_id,
        role="MEMBER"
    )

    db.add(new_member)
    db.commit()

    return {
        "message": "Đã thêm thành viên thành công!"
    }

# API 4: XÓA THÀNH VIÊN (Chỉ OWNER)

@router.delete("/{campaign_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    campaign_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Kiểm tra OWNER
    is_owner = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id,
        CampaignMember.role == "OWNER"
    ).first()

    if not is_owner:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền! Chỉ OWNER mới được xóa thành viên."
        )

    # Tìm member cần xóa
    member_to_remove = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == user_id
    ).first()

    if not member_to_remove:
        raise HTTPException(
            status_code=404,
            detail="Người này không có trong chiến dịch!"
        )

    # Không được xóa OWNER cuối cùng
    if member_to_remove.role == "OWNER":

        owner_count = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.role == "OWNER"
        ).count()

        if owner_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Không thể xóa OWNER cuối cùng!"
            )

    db.delete(member_to_remove)
    db.commit()

    return

# API 5: XEM DANH SÁCH THÀNH VIÊN

@router.get(
    "/{campaign_id}/members",
    response_model=List[CampaignMemberResponse]
)
def get_campaign_members(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Kiểm tra user có trong campaign không
    is_member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền! Chỉ thành viên mới được xem."
        )

    members = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id
    ).all()

    return members