# Convert google calendar busy times into available slots for clients to book

from datetime import datetime, time, timedelta
import pytz

# FreeBusy API will give me a list of time ranges when the stylist is busy, represented as start and end datetimes in UTC. E.g.,
# busy_intervals = [(start_time_utc, end_time_utc), ...]


def normalize_intervals(intervals):
    """Sort and merge overlapping or touching busy intervals
        Example:
        [(10:00, 11:00), (10:30, 11:30)] → [(10:00, 11:30)]"""
    if not intervals:
        return []
    # note to self: i drew a diagram to understand this algorithm, refer back to it if confused. taken on iphone 091625
    # ***Sort intervals by start time***
    # A lambda function is a small, anonymous function defined in a single line. It can take any number of arguments but can only have one expression, which is evaluated and returned.
    # In key=lambda x: expression, the lambda function is applied to each item x in the iterable being sorted. The result of expression for each x is then used as the basis for comparison during the sorting process.
    # the x[0] means to sort by the first element of each tuple (the start time)
    intervals.sort(key=lambda x: x[0])
    # start with the first interval now that they're sorted
    merged = [intervals[0]]

    # ***Merge overlapping or touching intervals***
    # [1:] means start at index 1 (the second item) and go to the end
    # we can destructure the tuple directly in the for loop! :) omg yay python
    for current_start, current_end in intervals[1:]:
        # get the last merged interval ([-1:] means last item in list). to start, merged only has one item (the first interval)
        last_start, last_end = merged[-1]
        # if the current interval starts before or when the last merged one ends, they overlap or touch
        if current_start <= last_end:
          # merge them by updating the end time of the last merged interval to be the later of the two end times. i don't understand how we can update a tuple like this??? it's immutable??? ....well, it's because we're creating a new tuple and reassigning it to the last position in the list
            merged[-1] = (last_start, max(last_end, current_end))
        else:  # if they don't overlap, just add the current interval to the merged list as is
            merged.append((current_start, current_end))

    return merged


def generate_available_slots(service_duration, busy_intervals, date, slot_granularity=15):
    """ Turns a list of busy intervals into available slots for booking.
    """
    # 1.) Define working hours for a day in CST
    central = pytz.timezone('America/Chicago')  # Central Time Zone object
    # central.localize() makes a naive datetime (no timezone info) into an aware datetime (with timezone info)
    # combine() makes a datetime from a date object and a time object
    day_start_ct = central.localize(
        datetime.combine(date, time(9, 0)))  # 9:00 AM CST
    day_end_ct = central.localize(
        datetime.combine(date, time(17, 0)))  # 5:00 PM CST

    # 2.) Convert above to UTC for comparison with busy times from Google Calendar
    day_start = day_start_ct.astimezone(pytz.utc)
    day_end = day_end_ct.astimezone(pytz.utc)

    # 3.) Busy intervals may not be in order or may overlap, so first merge any overlapping busy intervals, and then sort them by start time (via helper function above).
    busy_intervals = normalize_intervals(busy_intervals)

    # 4.) Subtract busy intervals from working hours to get free time intervals
    free_intervals = []
    current_start = day_start  # start with the beginning of the work day
    for start, end in busy_intervals:
        # if opening time is less than (before) the busy interval's start time, then there's free time from current_start to the start of the busy interval, so add that as a free interval (it will be the gap before the busy interval). Note to self: I also drew a diagram to understand this logic, refer back to it if confused. pic taken on iphone 091625
        if current_start < start:
            free_intervals.append((current_start, start))
        # move the current_start forward to the end of the busy interval (if it's later than the current_start, which it always should be given my setup... but this is a safty net i guess so we don't accidentally reset current_start backwards... it can only move farwards.)
        if end > current_start:  # safety check, this should always be true given my setup
            current_start = end

    # 5.) After the last busy interval, there might still be free time until day_end, so add that as a free interval if applicable.
    if current_start < day_end:
        free_intervals.append((current_start, day_end))

    # 6. Slice the free intervals into into bookable slots that match the service's duration
    slots = []
    step = timedelta(minutes=slot_granularity)  # default is 15 min increments
    for free_start, free_end in free_intervals:
        slot_start = free_start
        # while the slot (from slot_start to slot_start + service_duration) fits within the free interval
        while slot_start + timedelta(minutes=service_duration) <= free_end:
          # set the slot end time
            slot_end = slot_start + timedelta(minutes=service_duration)
            # add the slot to the list
            slots.append((slot_start, slot_end))
            # move the slot_start forward by the step (default 15 min)
            # note: this means slots can overlap if service_duration > slot_granularity (true for  most if not all hair services)
            slot_start += step

    # 7.) Return all the slots (in UTC since that's how we store times in the DB)
    return slots
