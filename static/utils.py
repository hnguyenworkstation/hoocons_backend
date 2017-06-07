import hashlib
import re
from datetime import datetime
import urllib.request


def date_from_iso8601(date_time_str):
    if date_time_str != None and date_time_str != "":
        return datetime.strptime(date_time_str, "%Y-%m-%d")
    else:
        return None


def toISO8601(datetime):
    # if datetime != None and datetime != "":
    return str(datetime)
    #     return datetime.strptime(str(datetime), '%Y-%m-%d %H:%M:%S').isoformat()
    # else:
    #     return ""


def computeMD5hash(string):
    str_encode = string + string[4:] + str(datetime.utcnow().hour)
    print(" a " + str_encode)
    m = hashlib.md5()
    m.update(str_encode.encode('utf-8'))
    return m.hexdigest()


def getMD5HashRegister(string):
    str = string + "*&/asd].``~"
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()


def get_default_avatar_url():
    return 'http://res.cloudinary.com/dumfykuvl/image/upload/v1493749974/images_lm0sjf.jpg'


def haveSpecialCharacter(string):
    return False if re.match("^[a-zA-Z0-9_]*$", string) else True


def haveSpecialCharacterIgnoreA(string):
    if string[0] != '@':
        return True
    str1 = string[1:]
    return haveSpecialCharacter(str1)


def getTypeString(string):
    try:
        with urllib.request.urlopen(string) as response:
            info = response.info()
            print(info.get_content_type())  # -> text/html
            print(info.get_content_maintype())  # -> text
            print(info.get_content_subtype())
            if (info.get_content_maintype() == 'text'):
                return "Web"
            if info.get_content_maintype() == 'image':
                return "Image"
    except Exception as e:
        print(str(e))
        return "Text"
