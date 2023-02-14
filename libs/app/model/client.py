

class Client:
    """
        Class of type Client used to represent the 
        entity client that's going to used the 
        system services
    """
    def __init__(self, name: str, number: str):
        if len(number) < 8 or number.isdigit() is False:
            raise TypeError('Enter a valid Number!')
        else:
            self.phone_number = number
        self.name = name
        self.exists = False
