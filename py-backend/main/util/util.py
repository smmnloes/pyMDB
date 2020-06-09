import bisect

from unidecode import unidecode


def tid_nid_to_int(tid_nid):
    return int(tid_nid[2:])


def ordered_list_contains_number(value, ordered_list):
    i = bisect.bisect_left(ordered_list, value)
    if i != len(ordered_list) and ordered_list[i] == value:
        return True
    else:
        return False


def clean_nulls(entries):
    return [None if entry == '\\N' else entry for entry in entries]

def normalize(to_normalize):
    return unidecode(to_normalize).lower()

