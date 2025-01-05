from datetime import datetime

def date_to_type(date: str, time: str):
    current_year = str(datetime.now().year)
    datetime_str = date + '/' + current_year + ' ' + time + ':00'
    return datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
