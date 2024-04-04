from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Rule, User
from src.schemas.rule_schema import RulePatchSchema, RulePostSchema, RuleResponseSchema
from src.services import rule_service
from src.services.auth_service import get_current_user


router = APIRouter(
    # routing prefix
    prefix="/rules",
    # documentation tag
    tags=["rules"],
    # default response
    #responses={404: {"route": "Not found"}},
)

@router.get("/all", response_model=list[RuleResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_rules(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Rule]:
    return rule_service.get_all_rules(db)

@router.get("/{id}", response_model=RuleResponseSchema, status_code=status.HTTP_200_OK)
async def get_rule(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Rule:
    return rule_service.get_rule_by_id(id, db)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_rule(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    return rule_service.delete_rule(id, db)

@router.post("/", response_model=RuleResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_rule(rule_post_schema: RulePostSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Rule:
    return rule_service.create_rule(rule_post_schema, db)

@router.patch("/{id}", response_model=RuleResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_rule(id: str, rule_patch_schema: RulePatchSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Rule:
    return rule_service.update_rule(id, rule_patch_schema, db)
