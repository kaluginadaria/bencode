import re


class BencodeParseException(Exception):
    def __init__(self):
        self.message = 'can not parse'

    def __str__(self):
        return self.message


class Bencode:
    def __init__(self, coding='UTF-8'):
        self.coding = coding

    def decode(self, input_string):
        input_string = input_string.encode(self.coding)
        value, end_pos = self.call_parser(input_string)
        if end_pos != len(input_string):
            raise BencodeParseException()
        return value

    def call_parser(self, content):
        first_symbol = content[:1]
        if first_symbol in self.PARSER_DICT.keys():
            value, next_pos = self.PARSER_DICT[first_symbol](self, content)
            return value, next_pos
        return None, 0

    def parse_dict(self, dict_string):
        content = dict_string[1:]
        result = {}
        key, next_pos = self.call_parser(content)
        if key:
            value, diff_pos = self.call_parser(content[next_pos:])
            next_pos += diff_pos
            while key and value is not None:
                result[key] = value
                key, diff_pos = self.call_parser(content[next_pos:])
                next_pos += diff_pos
                value, diff_pos = self.call_parser(content[next_pos:])
                next_pos += diff_pos

        return result, next_pos + 2

    def parse_list(self, list_string):
        result = []
        content = list_string[1:]
        value, next_pos = self.call_parser(content)

        while value is not None:
            result.append(value)
            value, diff_pos = self.call_parser(content[next_pos:])
            next_pos += diff_pos

        return result, next_pos + 2

    def parse_str(self, str_string):
        match_str = re.match(rb'^([0-9]+):(.*)', str_string)
        if match_str:
            amount = int(match_str.group(1))
            value = bytes(match_str.group(2)[:amount])
            end_pos = match_str.span(2)[0] + amount
            value = value.decode(self.coding)
            return value, end_pos
        else:
            raise BencodeParseException()

    def parse_int(self, int_string):
        match_int = re.match(rb'^i(-?[0-9]+)e', int_string)
        if match_int:
            value = int(match_int.group(1))
            end_pos = match_int.span(1)[1] + 1
            return value, end_pos
        else:
            raise BencodeParseException()

    PARSER_DICT = {
        b'i': parse_int,
        b'l': parse_list,
        b'd': parse_dict,
        b'0': parse_str,
        b'1': parse_str,
        b'2': parse_str,
        b'3': parse_str,
        b'4': parse_str,
        b'5': parse_str,
        b'6': parse_str,
        b'7': parse_str,
        b'8': parse_str,
        b'9': parse_str,
    }
