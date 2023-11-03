import unittest


def validate_current_time(current_time: int) -> None:
    """
    Validate the current time.

    Args:
    current_time: An integer representing the current time in 24-hour format (0000-2359).

    Raises:
    ValueError: If the current time is not an integer or not in the expected range.
    """
    if not isinstance(current_time, int) or not 0 <= current_time < 2400:
        raise ValueError("Current time must be an integer between 0 and 2399.")


def validate_day(day: int) -> None:
    """
    Validate the day of the week.

    Args:
    day: An integer representing the day of the week (0=Sunday, 6=Saturday).

    Raises:
    ValueError: If the day is not an integer or not within the range of [0, 6].
    """
    if not isinstance(day, int) or not 0 <= day < 7:
        raise ValueError("Day must be an integer between 0 and 6.")


def validate_hours(hours: dict) -> None:
    """
    Validate the hours dictionary structure.

    Args:
    hours: A dictionary with keys as integers (0-6) for days and values as lists of
           dictionaries containing 'open' and 'close' times.

    Raises:
    ValueError: If hours is not a dictionary, if day keys are not in the correct range, or if
                intervals are not properly formatted with 'open' and 'close' times.
    """
    if not isinstance(hours, dict):
        raise ValueError("Hours must be a dictionary.")
    if not all(isinstance(day, int) and 0 <= day < 7 for day in hours.keys()):
        raise ValueError("Hours dictionary must have integer keys between 0 and 6.")
    for intervals in hours.values():
        if not isinstance(intervals, list):
            raise ValueError("Hours intervals must be provided as a list.")
        for interval in intervals:
            if not isinstance(interval, dict):
                raise ValueError("Each interval must be a dictionary.")
            if not all(key in interval for key in ["open", "close"]):
                raise ValueError("Each interval must have 'open' and 'close' keys.")
            for time in interval.values():
                validate_current_time(time)


def is_within_hours(interval: dict, current_time: int) -> bool:
    """
    Check if the current time is within a given open-close interval.

    Args:
    interval: A dictionary with 'open' and 'close' times.
    current_time: The current time to check against the interval.

    Returns:
    bool: True if the current time is within the interval, False otherwise.
    """
    validate_current_time(current_time)
    open_time, close_time = interval["open"], interval["close"]
    # If close time is less than open time, it indicates the interval spans past midnight.
    if close_time < open_time:
        return current_time >= open_time or current_time < close_time
    return open_time <= current_time < close_time


def is_open(current_time: int, day: int, hours: dict) -> bool:
    """
    Determine if the store is open based on the current time and day.

    Args:
    current_time: The current time in 24-hour format (0000-2359).
    day: The current day of the week (0=Sunday, 6=Saturday).
    hours: The store's hours of operation as a dictionary with days as keys and a list of
           open-close intervals as values.

    Returns:
    bool: True if the store is currently open, False otherwise.
    """
    validate_current_time(current_time)
    validate_day(day)
    validate_hours(hours)

    # Check current day's hours
    if day in hours:
        for interval in hours[day]:
            if is_within_hours(interval, current_time):
                return True

    # Check previous day's hours in case the store is open past midnight
    previous_day = (day - 1) % 7
    if previous_day in hours:
        for interval in hours[previous_day]:
            if (
                interval["close"] < interval["open"]
            ):  # Check if the store closes after midnight
                if (
                    current_time < interval["close"]
                ):  # The time should be less than the closing time
                    return True

    # If none of the conditions above are met, assume the store is closed
    return False


class TestStoreHoursFunctions(unittest.TestCase):
    def setUp(self):
        # Setup a sample hours dictionary that will be used across multiple tests.
        self.hours = {
            0: [{"open": 800, "close": 1500}, {"open": 1700, "close": 200}],
            2: [{"open": 800, "close": 1200}, {"open": 1500, "close": 2100}],
            3: [{"open": 800, "close": 2100}],
            4: [{"open": 800, "close": 0}],
            5: [{"open": 800, "close": 2100}],
            6: [{"open": 800, "close": 1300}, {"open": 1700, "close": 200}],
        }

    def test_validate_current_time(self):
        # Test valid current time
        self.assertIsNone(validate_current_time(2359))

        # Test invalid current times
        with self.assertRaises(ValueError):
            validate_current_time(2400)
        with self.assertRaises(ValueError):
            validate_current_time(-1)
        with self.assertRaises(ValueError):
            validate_current_time("100")

    def test_validate_day(self):
        # Test valid day
        self.assertIsNone(validate_day(6))

        # Test invalid days
        with self.assertRaises(ValueError):
            validate_day(7)
        with self.assertRaises(ValueError):
            validate_day(-1)
        with self.assertRaises(ValueError):
            validate_day("Monday")

    def test_validate_hours(self):
        # Test valid hours
        self.assertIsNone(validate_hours(self.hours))

        # Test invalid hours
        with self.assertRaises(ValueError):
            validate_hours("Not a dictionary")
        with self.assertRaises(ValueError):
            validate_hours({7: [{"open": 800, "close": 2100}]})
        with self.assertRaises(ValueError):
            validate_hours({0: "Not a list"})
        with self.assertRaises(ValueError):
            validate_hours({0: [{"open": 800}]})

    def test_is_within_hours(self):
        # Test a time within open hours
        self.assertTrue(is_within_hours({"open": 800, "close": 1700}, 1200))

        # Test a time outside of open hours
        self.assertFalse(is_within_hours({"open": 800, "close": 1700}, 1800))

        # Test a time within an interval that spans past midnight
        self.assertTrue(is_within_hours({"open": 1700, "close": 200}, 100))

    def test_is_open(self):
        # Test times when the store should be open
        self.assertTrue(is_open(current_time=800, day=0, hours=self.hours))
        self.assertTrue(is_open(current_time=1800, day=0, hours=self.hours))
        self.assertTrue(is_open(current_time=100, day=1, hours=self.hours))

        # Test times when the store should be closed
        self.assertFalse(is_open(current_time=1600, day=0, hours=self.hours))


if __name__ == "__main__":
    unittest.main()
