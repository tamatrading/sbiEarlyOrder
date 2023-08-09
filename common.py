
def toValue(f_str: str):
    if f_str.find(',') >= 0:
        f_tmp = int(f_str.replace(",", ""))
    else:
        f_tmp = int(f_str)
    return f_tmp

def kehaiValue(f_str: str):
    f_spl = f_str.split()
    f_len = len(f_spl)

    if f_len == 2:
        return f_spl[0], toValue(f_spl[1])
    elif f_len == 1:
        return "", toValue(f_spl[0])
    else:
        return "", -1
