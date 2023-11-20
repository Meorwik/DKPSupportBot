from loader import postgres_manager
from data.assessments.assessments_manager import \
    PkpAssessment, \
    HivRiskAssessment, \
    HivKnowledgeAssessment, \
    UnderstandingPLHIVAssessment, \
    SogiAssessment, \
    ASSESSMENTS_NAMES

ADDITIONAL_INFO_MONTH = """
*В этом месяце:*
--  Присоединилось {users_in_month} чел
--  Обратились к консультанту {people_consultant} чел
"""

ASSESSMENTS_NUMBERS = {f"assessment_{key + 1}": value for key, value in enumerate(ASSESSMENTS_NAMES.keys())}

ADDITIONAL_INFO_EMPTY = ""

ANALYTICS_TEMPLATE = """
**Общая аналитика за {date}**

**Всего человек в боте:** {all_users_count}
**Оценка консультанта:** {consultant_rating} / 5

{additional}

**Аналитика по тестам:**

**{assessment_1_name}:**
Начали тест: {assessment_1_started}
Завершили тест: {assessment_1_finished}

**{assessment_2_name}:**
Начали тест: {assessment_2_started}
Завершили тест: {assessment_2_finished}

**{assessment_3_name}:**
Начали тест: {assessment_3_started}
Завершили тест: {assessment_3_finished}

**{assessment_4_name}:**
Начали тест: {assessment_4_started}
Завершили тест: {assessment_4_finished}

**{assessment_5_name}:**
Начали тест: {assessment_5_started}
Завершили тест: {assessment_5_finished}
"""


class AnalyticsStorage:
    def __init__(self):
        self.analytics_template = ANALYTICS_TEMPLATE
        self.additional_info = ADDITIONAL_INFO_EMPTY

        self.assessment_1_name = HivRiskAssessment.get_assessment_name()
        self.assessment_2_name = SogiAssessment.get_assessment_name()
        self.assessment_3_name = PkpAssessment.get_assessment_name()
        self.assessment_4_name = HivKnowledgeAssessment.get_assessment_name()
        self.assessment_5_name = UnderstandingPLHIVAssessment.get_assessment_name()

        self.all_users_count = None

        self.assessment_1_started = None
        self.assessment_1_finished = None

        self.assessment_2_started = None
        self.assessment_2_finished = None

        self.assessment_3_started = None
        self.assessment_3_finished = None

        self.assessment_4_started = None
        self.assessment_4_finished = None

        self.assessment_5_started = None
        self.assessment_5_finished = None

        self.consultant_rating = None
        self.users_in_month = None
        self.people_consultant = None


# КЛАСС AnalyticsManager
# Создан для работы с аналитикой жизнедеятельности данного продукта
class AnalyticsManager:
    def __init__(self):
        self.current_db = postgres_manager
        self.storage = AnalyticsStorage()
        self.date = None

    async def __set_assessment_1_started_statistic(self, assessment_name, period=None):
        self.storage.assessment_1_started = await self.current_db.get_assessment_started_statistic(assessment_name, period)

    async def __set_assessment_2_started_statistic(self, assessment_name, period=None):
        self.storage.assessment_2_started = await self.current_db.get_assessment_started_statistic(assessment_name, period)

    async def __set_assessment_3_started_statistic(self, assessment_name, period=None):
        self.storage.assessment_3_started = await self.current_db.get_assessment_started_statistic(assessment_name, period)

    async def __set_assessment_4_started_statistic(self, assessment_name, period=None):
        self.storage.assessment_4_started = await self.current_db.get_assessment_started_statistic(assessment_name, period)

    async def __set_assessment_5_started_statistic(self, assessment_name, period=None):
        self.storage.assessment_5_started = await self.current_db.get_assessment_started_statistic(assessment_name, period)

    async def __set_assessment_1_finished_statistic(self, assessment_name, period=None):
        self.storage.assessment_1_finished = await self.current_db.get_assessment_finished_statistic(assessment_name, period)

    async def __set_assessment_2_finished_statistic(self, assessment_name, period=None):
        self.storage.assessment_2_finished = await self.current_db.get_assessment_finished_statistic(assessment_name, period)

    async def __set_assessment_3_finished_statistic(self, assessment_name, period=None):
        self.storage.assessment_3_finished = await self.current_db.get_assessment_finished_statistic(assessment_name, period)

    async def __set_assessment_4_finished_statistic(self, assessment_name, period=None):
        self.storage.assessment_4_finished = await self.current_db.get_assessment_finished_statistic(assessment_name, period)

    async def __set_assessment_5_finished_statistic(self, assessment_name, period=None):
        self.storage.assessment_5_finished = await self.current_db.get_assessment_finished_statistic(assessment_name, period)

    async def __set_average_consultant_rating(self):
        self.storage.consultant_rating = await self.current_db.get_average_consultant_rating()

    async def __set_all_users_count(self):
        self.storage.all_users_count = await self.current_db.get_all_users_count()

    async def __set_new_registered_users_count(self, period):
        self.storage.users_in_month = await self.current_db.get_users_count_in_month(period)

    async def __set_users_count_contacted_consultant_in_period(self, period):
        self.storage.people_consultant = await self.current_db.get_count_contacted_consultant(period)

    async def __set_additional_info_month(self, users_in_month, people_consultant):
        self.storage.additional_info = ADDITIONAL_INFO_MONTH.format(
            users_in_month=users_in_month,
            people_consultant=people_consultant
        )

    async def analyze_all(self):
        self.date = "все время"
        await self.__set_all_users_count()
        await self.__set_average_consultant_rating()

        await self.__set_assessment_1_started_statistic(ASSESSMENTS_NUMBERS["assessment_1"])
        await self.__set_assessment_2_started_statistic(ASSESSMENTS_NUMBERS["assessment_2"])
        await self.__set_assessment_3_started_statistic(ASSESSMENTS_NUMBERS["assessment_3"])
        await self.__set_assessment_4_started_statistic(ASSESSMENTS_NUMBERS["assessment_4"])
        await self.__set_assessment_5_started_statistic(ASSESSMENTS_NUMBERS["assessment_5"])

        await self.__set_assessment_1_finished_statistic(ASSESSMENTS_NUMBERS["assessment_1"])
        await self.__set_assessment_2_finished_statistic(ASSESSMENTS_NUMBERS["assessment_2"])
        await self.__set_assessment_3_finished_statistic(ASSESSMENTS_NUMBERS["assessment_3"])
        await self.__set_assessment_4_finished_statistic(ASSESSMENTS_NUMBERS["assessment_4"])
        await self.__set_assessment_5_finished_statistic(ASSESSMENTS_NUMBERS["assessment_5"])

    async def analyze_period(self, period):
        self.date = period

        await self.__set_all_users_count()
        await self.__set_average_consultant_rating()

        await self.__set_users_count_contacted_consultant_in_period(period)
        await self.__set_new_registered_users_count(period)
        await self.__set_additional_info_month(self.storage.users_in_month, self.storage.people_consultant)

        await self.__set_assessment_1_started_statistic(ASSESSMENTS_NUMBERS["assessment_1"], period)
        await self.__set_assessment_2_started_statistic(ASSESSMENTS_NUMBERS["assessment_2"], period)
        await self.__set_assessment_3_started_statistic(ASSESSMENTS_NUMBERS["assessment_3"], period)
        await self.__set_assessment_4_started_statistic(ASSESSMENTS_NUMBERS["assessment_4"], period)
        await self.__set_assessment_5_started_statistic(ASSESSMENTS_NUMBERS["assessment_5"], period)

        await self.__set_assessment_1_finished_statistic(ASSESSMENTS_NUMBERS["assessment_1"], period)
        await self.__set_assessment_2_finished_statistic(ASSESSMENTS_NUMBERS["assessment_2"], period)
        await self.__set_assessment_3_finished_statistic(ASSESSMENTS_NUMBERS["assessment_3"], period)
        await self.__set_assessment_4_finished_statistic(ASSESSMENTS_NUMBERS["assessment_4"], period)
        await self.__set_assessment_5_finished_statistic(ASSESSMENTS_NUMBERS["assessment_5"], period)

    async def get_analytics_results(self):
        analytics = self.storage.analytics_template.format(
            date=self.date,
            all_users_count=self.storage.all_users_count,
            consultant_rating=self.storage.consultant_rating,

            assessment_1_name=self.storage.assessment_1_name,
            assessment_2_name=self.storage.assessment_2_name,
            assessment_3_name=self.storage.assessment_3_name,
            assessment_4_name=self.storage.assessment_4_name,
            assessment_5_name=self.storage.assessment_5_name,

            assessment_1_started=self.storage.assessment_1_started,
            assessment_2_started=self.storage.assessment_2_started,
            assessment_3_started=self.storage.assessment_3_started,
            assessment_4_started=self.storage.assessment_4_started,
            assessment_5_started=self.storage.assessment_5_started,

            assessment_1_finished=self.storage.assessment_1_finished,
            assessment_2_finished=self.storage.assessment_2_finished,
            assessment_3_finished=self.storage.assessment_3_finished,
            assessment_4_finished=self.storage.assessment_4_finished,
            assessment_5_finished=self.storage.assessment_5_finished,

            additional=self.storage.additional_info
        )

        return analytics
