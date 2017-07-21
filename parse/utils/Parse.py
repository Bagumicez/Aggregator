from . import Freelance
from . import Freelansim
from . import Weblancer
from . import Fl


def start_parse(source):
    if source == 'freelance':
        result = Freelance.main()
    elif source == 'fl':
        result = Fl.main()
    elif source == 'freelansim':
        result = Freelansim.main()
    elif source == 'weblancer':
        result = Weblancer.main()
    return result


def main():
    print(start_parse('freelance'))


if __name__ == '__main__':
    main()
