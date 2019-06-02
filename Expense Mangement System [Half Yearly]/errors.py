class Error(Exception):
    pass

class SmallPasswordError(Error):
    def __init__(self, password, explanantion) :
        self.password = password
        self.explanantion = "Password less than 8 characters"
# password 
# try:
#     raise smallPasswordError('abcdefghijkl',"")
# except smallPasswordError as s:
#     print("Exception occurred: smallPasswordError",s.explanantion)
