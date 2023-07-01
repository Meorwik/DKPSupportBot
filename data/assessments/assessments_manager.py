from . import understanding_PLHIV_assessment
from . import hiv_knowledge_assessment
from . import hiv_risk_assessment
from . import pkp_assessment
from . import sogi_assessment

ASSESSMENTS_LANGUAGES_CALLBACKS = [
    "ru_hiv_risk_assessment",
    "kz_hiv_risk_assessment",

    "ru_sogi_assessment",
    "kz_sogi_assessment",

    "ru_pkp_assessment",
    "kz_pkp_assessment",

    "ru_hiv_knowledge_assessment",
    "kz_hiv_knowledge_assessment",

    "ru_understanding_PLHIV_assessment",
    "kz_understanding_PLHIV_assessment"
]

ASSESSMENTS_NAMES = {
    "hiv_risk_assessment": "Оценка риска инфицирования ВИЧ 📋",
    "sogi_assessment": "Оценка знаний на тему СОГИ 📋",
    "pkp_assessment": "Тестирование ПКП 📋",
    "hiv_knowledge_assessment": "Оценка знаний о ВИЧ 📋",
    "understanding_PLHIV_assessment": "Тестирование на понимание ЛЖВ 📋",
}


WRONG_POSSIBLE_ASSESSMENT_TYPE = "WRONG_POSSIBLE"
WRONG_IMPOSSIBLE_ASSESSMENT_TYPE = "WRONG_IMPOSSIBLE"


class Assessment:
    _assessment_name = ASSESSMENTS_NAMES

    def get_ru_version(self):
        return {"result_ratings": self.result_ratings_ru,
                "questions": self.questions_ru,
                "type": self.assessment_type}

    def get_kz_version(self):
        return {"result_ratings": self.result_ratings_kz,
                "questions": self.questions_kz,
                "type": self.assessment_type}

    @classmethod
    def get_assessment_name(cls):
        return cls._assessment_name


class HivRiskAssessment(Assessment):
    def __init__(self):
        self.assessment_type = WRONG_IMPOSSIBLE_ASSESSMENT_TYPE

        self.questions_kz = hiv_risk_assessment.questions_kz
        self.questions_ru = hiv_risk_assessment.questions_ru

        self.result_ratings_kz = hiv_risk_assessment.risk_ratings_kz
        self.result_ratings_ru = hiv_risk_assessment.risk_ratings_ru

    _assessment_name = ASSESSMENTS_NAMES["hiv_risk_assessment"]


class SogiAssessment(Assessment):
    def __init__(self):
        self.assessment_type = WRONG_POSSIBLE_ASSESSMENT_TYPE

        self.questions_kz = None
        self.questions_ru = sogi_assessment.questions_ru

        self.result_ratings_kz = None
        self.result_ratings_ru = sogi_assessment.result_ratings_ru

    _assessment_name = ASSESSMENTS_NAMES["sogi_assessment"]


class PkpAssessment(Assessment):
    def __init__(self):
        self.assessment_type = WRONG_POSSIBLE_ASSESSMENT_TYPE

        self.questions_kz = None
        self.questions_ru = pkp_assessment.questions_ru

        self.result_ratings_kz = None
        self.result_ratings_ru = pkp_assessment.result_ratings_ru

    _assessment_name = ASSESSMENTS_NAMES["pkp_assessment"]


class UnderstandingPLHIVAssessment(Assessment):
    def __init__(self):
        self.assessment_type = WRONG_POSSIBLE_ASSESSMENT_TYPE

        self.questions_kz = None
        self.questions_ru = understanding_PLHIV_assessment.questions_ru

        self.result_ratings_kz = None
        self.result_ratings_ru = understanding_PLHIV_assessment.result_ratings_ru

    _assessment_name = ASSESSMENTS_NAMES["understanding_PLHIV_assessment"]


class HivKnowledgeAssessment(Assessment):
    def __init__(self):
        self.assessment_type = WRONG_POSSIBLE_ASSESSMENT_TYPE

        self.questions_kz = None
        self.questions_ru = hiv_knowledge_assessment.questions_ru

        self.result_ratings_kz = None
        self.result_ratings_ru = hiv_knowledge_assessment.result_ratings_ru

    _assessment_name = ASSESSMENTS_NAMES["hiv_knowledge_assessment"]
