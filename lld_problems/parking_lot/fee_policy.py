from datetime import datetime
import math

class FeePolicy:

    WEEKDAY_RATE = 50
    WEEKEND_RATE = 70
    SPECIAL_DATES = {"2025-12-25": 150}

    @staticmethod
    def calculate_fee(start_time, end_time):
        hours = (end_time - start_time).total_seconds() / 3600
        today = datetime.now().date().isoformat()
        if today in FeePolicy.SPECIAL_DATES:
            rate = FeePolicy.SPECIAL_DATES[today]
        elif datetime.now().weekday() >= 5:
            rate = FeePolicy.WEEKEND_RATE
        else:
            rate = FeePolicy.WEEKDAY_RATE

        return math.ceil(hours) * rate
