import argparse

arg_parser = argparse.ArgumentParser(description="Description: "
                                                 "A mock pipeline to simulate sources.")

arg_parser.add_argument('-m', '--msr_set', type=str, metavar="", required=True,
                        help="measurement set filename (in resources folder)")
arg_parser.add_argument('-l', '--cat_list', nargs='+', metavar="", required=True,
                        help='cat filename list (in resources folder)')

group = arg_parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', action='store_true', help='print quietly(default)')
group.add_argument('-v', '--verbose', action='store_true', help='print verbose')
