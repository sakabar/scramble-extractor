"""Extract hard scrambles from cstimer stats informatino

usage: extract_hard_scramble.py <total_threshold> [<multiphase_threshold_list>...]
"""

import logging
import sys

from docopt import docopt

from info.saxcy.scramble_extractor.extractor import Extractor


def main():
    logging.basicConfig(level=logging.WARNING)

    args = docopt(__doc__)
    total_threshold = float(args["<total_threshold>"])
    multiphase_threshold_list = map(float, args["<multiphase_threshold_list>"])

    extractor = Extractor(total_threshold=total_threshold,
                          multiphases_threshold_list=multiphase_threshold_list)
    for line in sys.stdin:
        line = line.rstrip()
        solve_results = extractor.pickup_result_from_lines([line])
        if len(solve_results) == 1:
            print(solve_results[0].scramble)
            # print(solve_results[0].total_sec)

    return 0


if __name__ == '__main__':
    sys.exit(main())
