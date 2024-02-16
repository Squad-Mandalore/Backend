from datetime import datetime

def update_properties(self: Base, schema, db: Session):
    now = datetime.now()
    for attr, value in schema.__dict__.items():
        if value is not None:
            setattr(self, attr, value)
    self.last_edited_at = now
    db.commit()