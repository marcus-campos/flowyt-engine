class DotMap:
    def __init__(self, dictionary):
        self.__to_dotmap(dictionary)

    def __repr__(self):
        """"""
        return "<DotMap: %s=" ">" % self.__dict__

    def __to_dotmap(self, dictionary):
        for key in dictionary:
            if type(dictionary[key]) is dict:
                self.__to_dotmap(dictionary[key])
            setattr(self, key, dictionary[key])

    def to_dict(self):
        dictionary = self.__dict__
        return self.__dotmap_to_dict(dictionary)

    def __dotmap_to_dict(self, dictionary):
        for key in dictionary:
            if type(dictionary[key]) is dictionary:
                dictionary[key] = dictionary[key].__dict__
                dictionary = self.__dictionary_to_dict(dictionary[key])
        return dictionary
