from argparse import ArgumentParser
import re
import sys


LETTER_TO_NUMBER = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
}


class PhoneNumber:
    """
    
    """
    def __init__(self, number):
        if not isinstance(number, (str, int)):
            raise TypeError("PhoneNumber should be a string or integer")

        number_str = str(number)
        cleaned_number = re.sub(r"[^\dA-Za-z]", "", number_str.upper())
        converted_number = "".join(LETTER_TO_NUMBER.get(c, c) for c in cleaned_number)
        
        if not re.match(r"^(1)?[2-9]\d{2}[2-9](?!11)\d{2}\d{4}$", converted_number):
            raise ValueError("Invalid phone number")

        if len(converted_number) == 11:
            converted_number = converted_number[1:]

        self.area_code = converted_number[:3]
        self.exchange_code = converted_number[3:6]
        self.line_number = converted_number[6:]

    def __int__(self):
        """
        
        """
        return int(self.area_code + self.exchange_code + self.line_number)

    def __repr__(self):
        """
        
        """
        return f"PhoneNumber('{self.area_code + self.exchange_code + self.line_number}')"

    def __str__(self):
        """
        
        """
        return f"({self.area_code}) {self.exchange_code}-{self.line_number}"

    def __lt__(self, other):
        """
        
        """
        return int(self) < int(other)

def read_numbers(path):
    """
    
    """
    phone_number_list = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            name, number = line.strip().split("\t")
            try:
                phone_number = PhoneNumber(number)
                phone_number_list.append((name, phone_number))
            except ValueError:
                continue

    return sorted(phone_number_list, key=lambda x: x[1])



def main(path):
    """Read data from path and print results.
    
    Args:
        path (str): path to a text file. Each line in the file should consist of
            a name, a tab character, and a phone number.
    
    Side effects:
        Writes to stdout.
    """
    for name, number in read_numbers(path):
        print(f"{number}\t{name}")


def parse_args(arglist):
    """Parse command-line arguments.
    
    Expects one mandatory command-line argument: a path to a text file where
    each line consists of a name, a tab character, and a phone number.
    
    Args:
        arglist (list of str): a list of command-line arguments to parse.
        
    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of names and numbers")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
