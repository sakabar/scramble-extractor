import datetime
import re
from typing import List, Optional

from .constant import SolveResult


class Extractor:
    def __init__(self, total_threshold=0.0, multiphases_threshold_list=None, pickup_dnf=True):
        self._total_threshold = total_threshold
        if multiphases_threshold_list is None:
            self._multiphases_threshold_list = []
        else:
            self._multiphases_threshold_list = multiphases_threshold_list
        self._pickup_dnf = pickup_dnf

    def is_bad_solve(self, solve_result: SolveResult) -> bool:
        if solve_result is None:
            return False

        if not self._pickup_dnf and solve_result.is_dnf:
            return False

        if solve_result.total_sec >= self._total_threshold:
            return True

        if any([sec >= threshold for (sec, threshold) in zip(solve_result.multiphases, self._multiphases_threshold_list)]):
            return True

        return False

    @classmethod
    def extract(cls, line: str) -> Optional[SolveResult]:
        regexp = re.compile(r"""
        ^
        \d+\.\s+
        (?P<dnf>DNF)?
        \(?(?P<total>\d+\.\d+)\)? 
        =
        (?P<multiphases>\d+\.\d+(\+\d+\.\d+)+)
        \s{3}(?P<scramble>[UDLRFB].+)
        \s{3}@(?P<datetime>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})
        \s*
        $
        """, re.VERBOSE)
        matched = regexp.match(line)

        if not matched:
            return None

        is_dnf = matched.group('dnf') == 'DNF'
        total_sec = float(matched.group('total'))
        multiphases = [float(s) for s in matched.group('multiphases').split('+')]
        scramble = matched.group('scramble')
        dt = datetime.datetime.strptime(matched.group('datetime'), '%Y-%m-%d %H:%M:%S')

        return SolveResult(is_dnf=is_dnf,
                           total_sec=total_sec,
                           multiphases=multiphases,
                           scramble=scramble,
                           datetime=dt)

    def pickup_result_from_lines(self, lines: List[str]) -> List[SolveResult]:
        return [res for res in [self.extract(line) for line in lines] if self.is_bad_solve(res)]