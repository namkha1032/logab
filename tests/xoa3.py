def format_seconds(seconds):
    if seconds <= 0:
        return "0 seconds"
    
    units = [
        ("day", 86400),    # 24 * 60 * 60
        ("hour", 3600),    # 60 * 60
        ("minute", 60),
        ("second", 1)
    ]
    
    result = []
    for unit_name, unit_seconds in units:
        if seconds >= unit_seconds:
            value = seconds // unit_seconds
            seconds %= unit_seconds
            result.append(f"{value} {unit_name}{'s' if value > 1 else ''}")
    
    return " ".join(result)


# Example usage
test_seconds = [3661, 86400, 90001, 0, 3600]
for sec in test_seconds:
    print(f"{sec} seconds = {format_seconds(sec)}")