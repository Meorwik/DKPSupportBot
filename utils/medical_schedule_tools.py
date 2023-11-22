from keyboards.inline.inline_keyboards import SimpleKeyboardBuilder
from loader import postgres_manager, scheduler
from .misc.logging import logger, INFO
from aiogram import types


class Reminder:
    def __init__(self, user_id, drug_name, dose, time, reminder_id=None):
        self.reminder_id = reminder_id
        self.user_id = user_id
        self.drug_name = drug_name
        self.dose = dose
        self.time = time
        self.hour = self.time[0:self.time.index(":")]
        self.minute = self.time[self.time.index(":")+1:]

    async def get_message(self):
        return f"Напоминание !\nПримите {self.drug_name}\nДоза: {self.dose}"


class MedicalScheduleManager:
    __MEDICAL_REGISTRATION_INFO_TEMPLATE = \
        "<b>Номер записи:</b> <i>{id}</i>\n<b>Препарат:</b> <i>{drug_name}</i>\n<b>Доза:</b> <i>{dose}</i>\n<b>Когда:</b> <i>{time}</i>\n\n"
    __MEDICAL_REGISTRATIONS_EMPTY_CASE = "<b>Отсутствуют</b>"

    async def get_users_reminders_count(self, user):
        return len(await postgres_manager.get_users_medication_schedule_reminders(user))

    async def get_user_reminders_info(self, user):
        data = await postgres_manager.get_users_medication_schedule_reminders(user)
        text = ""

        if bool(data):
            registrations = [
                self.__MEDICAL_REGISTRATION_INFO_TEMPLATE.format(
                    id=registration["id"],
                    drug_name=registration["drug_name"],
                    dose=registration["dose"],
                    time=registration["time"]
                ) for registration in data
            ]

            for registration in registrations:
                text += registration

            return text

        else:
            return self.__MEDICAL_REGISTRATIONS_EMPTY_CASE


class Scheduler:

    async def clean_store(self):
        scheduler.remove_all_jobs()

    async def delete_reminder(self, reminder_id: int):
        scheduler.get_job(reminder_id).remove()

    async def set_reminder(self, reminder, message):
        async def send_reminder():
            await message.answer(
                text=await reminder.get_message(),
                reply_markup=SimpleKeyboardBuilder.get_note_taking_medications_keyboard(reminder.drug_name)
            )

        scheduler.add_job(
            func=send_reminder,
            trigger="cron",
            hour=reminder.hour,
            minute=reminder.minute,
            id=str(reminder.reminder_id)
        )

    async def set_reminders(self, reminders: list, message: types.Message):
        reminders_objects = [Reminder(
            reminder_id=reminder["id"],
            user_id=reminder["user_id"],
            drug_name=reminder['drug_name'],
            dose=reminder["dose"],
            time=reminder["time"]
        ) for reminder in reminders]

        for reminder in reminders_objects:
            await self.set_reminder(reminder, message)


