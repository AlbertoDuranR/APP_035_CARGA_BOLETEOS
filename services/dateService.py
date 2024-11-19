from datetime import datetime

class DateService:

    @staticmethod
    def dateToString(date):
        return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")