from . import hiv_risk_assessment

TESTS_LANGUAGES_CALLBACKS = ["ru_hiv_risk_assessment", "kz_hiv_risk_assessment"]


class HivRiskAssessment:
    def __init__(self):
        self.questions_kz = hiv_risk_assessment.questions_kz
        self.questions_ru = hiv_risk_assessment.questions_ru

        self.risk_ratings_kz = hiv_risk_assessment.risk_ratings_kz
        self.risk_ratings_ru = hiv_risk_assessment.risk_ratings_ru

    def get_ru_version(self):
        return {"risk_ratings": self.risk_ratings_ru,
                "questions": self.questions_ru}

    def get_kz_version(self):
        return {"risk_ratings": self.risk_ratings_kz,
                "questions": self.questions_kz}


