import re

def try_get_group(match, group_name):
    return match.groupdict().get(group_name) if match else None

re.try_get_group = try_get_group    