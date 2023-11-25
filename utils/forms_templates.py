from dataclasses import dataclass
from json import dumps, loads


class Form:
    def to_dict(self):
        return loads(dumps(self, default=lambda o: o.__dict__, indent=4, ensure_ascii=False))


@dataclass
class TestResults(Form):
    user_id: int = None
    test_name: str = None
    language: str = None
    is_finished: bool = None
    result: str = None
    datetime: str = None


@dataclass
class SetReminder(Form):
    drug_name: str = None
    dose: str = None
    time: str = None
