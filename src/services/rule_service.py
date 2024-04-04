from typing import cast
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Base, Rule
from src.schemas.rule_schema import RulePatchSchema, RulePostSchema
from src.services import update_service

def create_rule(rule_post_schema: RulePostSchema, db: Session) -> Rule:
    rule_dict = rule_post_schema.model_dump(exclude_unset=True)
    rule = Rule(**rule_dict)
    database_utils.add(rule, db)
    return rule

def get_rule_by_id(id: str, db: Session) -> Rule:
    rule: Base | None = db.get(Rule, id)

    if rule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")

    return cast(Rule, rule)

def update_rule(id: str, rule_patch_schema: RulePatchSchema, db: Session) -> Rule:
    rule: Base | None = db.get(Rule, id)

    if rule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")

    update_service.update_properties(rule, rule_patch_schema, db)
    return cast(Rule, rule)

def delete_rule(id: str, db: Session) -> None:
    return database_utils.delete(Rule, id, db)

def get_all_rules(db: Session) -> list[Rule]:
    return cast(list[Rule], database_utils.get_all(Rule, db))
