import re


def check(mobile, email):
    x = re.search("\A[\w]+[@][a-zA-z]+\.com\Z", email)
    y = re.search("\A[6789][0-9]{9}\Z", mobile)

    if (x):
        em = True
    else:
        em = False

    if (y):
        mo = True
    else:
        mo = False

    return mo, em
