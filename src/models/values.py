from datetime import datetime
import json

from sqlalchemy.orm import Session

from src.models.models import Category, Exercise, Gender, Rule
from src.logger.logger import logger

#value_dict: dict = {}

def parse_values(db: Session) -> None:
    with open('values.json', 'r', encoding='utf-8') as file:
        #global value_dict
        value_dict: dict = json.load(file)
        try:
            for category_data in value_dict['category']:
                category = Category(title=category_data['title'])
                db.add(category)
                db.flush()

                for exercise_data in category_data.get('exercise', []):
                    exercise = Exercise(
                        title=exercise_data['title'],
                        category_id=category.id,
                    )
                    db.add(exercise)
                    db.flush()

                    for rule_data in exercise_data.get('rules', []):
                        year_date = datetime.strptime(str(rule_data['year']), '%Y').date()

                        rule = Rule(
                            gender=Gender(rule_data['gender']),
                            from_age=rule_data['from_age'],
                            to_age=rule_data['to_age'],
                            bronze=rule_data['bronze'],
                            silver=rule_data['silver'],
                            gold=rule_data['gold'],
                            year=year_date,
                            exercise_id=exercise.id
                        )
                        db.add(rule)
                db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error while parsing values, {e}")

