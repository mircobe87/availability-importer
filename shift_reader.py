import datetime

SHIFTS_FILE='shifts.conf'
SHIFTS=None

def get_shifts():
    global SHIFTS
    if SHIFTS is None:
        SHIFTS = dict()
        with open(SHIFTS_FILE, 'r') as shifts_file:
            lines = shifts_file.readlines()
            for line in lines:
                if not line.startswith('#'):
                    values = line.split()
                    SHIFTS[values[0].strip().upper()] = {
                        'start_time': values[1].strip(),
                        'diration': int(values[2].strip())
                    }
            shifts_file.close()
    return SHIFTS

def read_availability(file_name):
    year = datetime.datetime.today().year
    shift_map = get_shifts()
    tz = datetime.datetime.utcnow().astimezone().tzinfo
    with open(file_name, 'r') as file:
        lines = file.readlines()
        file.close()
        headers = lines[0].split(',')
        shifts = lines[1].split(',')
        items = []
        for i in range(len(headers)):
            shift_key = shifts[i].strip().upper()
            if len(shift_key) > 0:
                date_str = headers[i].strip() + '/' + str(year)
                time_str = shift_map[shift_key]['start_time']
                shift_start = datetime.datetime.strptime(date_str + ' ' + time_str + ' ' + str(tz), "%d/%m/%Y %H:%M %Z")
                shift_end = shift_start + datetime.timedelta(hours=shift_map[shift_key]['diration'])
                timezone = 'Europe/Rome'
                items.append({
                    'name': shift_key,
                    'start': shift_start.astimezone(tz),
                    'end': shift_end.astimezone(tz),
                    'tz': str(tz)
                })
        items.sort(key=lambda x: x['start'])
        return items


