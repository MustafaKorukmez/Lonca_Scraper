from datetime import datetime, timezone, timedelta

class Utils:
    
    @staticmethod
    def get_current_time(self):
        # Get UTC timestamp
        now = datetime.now(timezone.utc)

        # Format microseconds
        now = now.replace(microsecond=(now.microsecond // 1000) * 1000)

        # Set timezone offset
        custom_timedelta = timedelta(hours=0, minutes=0)
        now_with_custom_offset = now.astimezone(timezone(custom_timedelta))
        return now_with_custom_offset
    