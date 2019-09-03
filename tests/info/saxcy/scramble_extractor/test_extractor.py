from datetime import datetime
from unittest import TestCase
import textwrap

from info.saxcy.scramble_extractor.constant import SolveResult
from info.saxcy.scramble_extractor.extractor import Extractor


class ExtractorTest(TestCase):
    def test_extract_normal(self):
        input_str = "3. 33.78=9.58+24.19   U B2 D2 F2 U' L2 B2 F2 L' D' U2 R D U B2 F U' F'   @2019-08-28 21:44:18 "
        actual = Extractor.extract(input_str)
        expected = SolveResult(is_dnf=False,
                               total_sec=33.78,
                               multiphases=[9.58, 24.19],
                               scramble="U B2 D2 F2 U' L2 B2 F2 L' D' U2 R D U B2 F U' F'",
                               datetime=datetime(2019, 8, 28, 21, 44, 18))
        self.assertEqual(actual, expected)

    def test_extract_none(self):
        input_str = "タイム一覧:"
        actual = Extractor.extract(input_str)
        self.assertIsNone(actual)

    def test_is_bad_1(self):
        input_str = "3. 33.78=9.58+24.19   U B2 D2 F2 U' L2 B2 F2 L' D' U2 R D U B2 F U' F'   @2019-08-28 21:44:18 "
        extractor = Extractor(total_threshold=30.0)
        solve_result = extractor.extract(input_str)
        actutal = extractor.is_bad_solve(solve_result)
        self.assertTrue(actutal)

    def test_is_bad_2(self):
        input_str = "3. 33.78=9.58+24.19   U B2 D2 F2 U' L2 B2 F2 L' D' U2 R D U B2 F U' F'   @2019-08-28 21:44:18 "
        extractor = Extractor(total_threshold=35.0)
        solve_result = extractor.extract(input_str)
        actutal = extractor.is_bad_solve(solve_result)
        self.assertFalse(actutal)

    def test_is_bad_3(self):
        input_str = "3. 33.78=9.58+24.19   U B2 D2 F2 U' L2 B2 F2 L' D' U2 R D U B2 F U' F'   @2019-08-28 21:44:18 "
        extractor = Extractor(total_threshold=35.0, multiphases_threshold_list=[10.0, 20.0])
        solve_result = extractor.extract(input_str)
        actutal = extractor.is_bad_solve(solve_result)
        self.assertTrue(actutal)

    def test_extract_2(self):
        input_str = "2. DNF(30.67)=9.02+21.65   B2 U2 F2 D L2 B2 U' L2 R2 B2 R' D2 F' R' U' F R B R' D2   @2019-08-28 21:42:36 "
        actual = Extractor.extract(input_str)
        expected = SolveResult(is_dnf=True,
                               total_sec=30.67,
                               multiphases=[9.02, 21.65],
                               scramble="B2 U2 F2 D L2 B2 U' L2 R2 B2 R' D2 F' R' U' F R B R' D2",
                               datetime=datetime(2019, 8, 28, 21, 42, 36))
        self.assertEqual(actual, expected)

    def test_extract_3(self):
        """
        合計タイムが1分を越えている場合
        :return:
        """
        input_str = "102. DNF(1:21.92)=20.04+1:01.87   L R U2 B2 U2 L' B2 L' D2 L' D2 F L' R' F' D L B' L2 D2 Fw' Uw'   @2019-08-31 22:10:36 "
        actual = Extractor.extract(input_str)
        expected = SolveResult(is_dnf=True,
                               total_sec=81.92,
                               multiphases=[20.04, 61.87],
                               scramble="L R U2 B2 U2 L' B2 L' D2 L' D2 F L' R' F' D L B' L2 D2 Fw' Uw'",
                               datetime=datetime(2019, 8, 31, 22, 10, 36))
        self.assertEqual(actual, expected)

    def test_extract_4(self):
        """
        +2を取られた場合の表記
        :return:
        """
        input_str = "105. 1:34.03+=17.31+1:14.70   U2 F' D2 B' L2 D2 L2 B2 L2 B L U F2 L' F U2 L2 B2 D2 Fw Uw'   @2019-09-01 11:52:17"
        actual = Extractor.extract(input_str)
        expected = SolveResult(is_dnf=False,
                               total_sec=94.03,
                               multiphases=[17.31, 74.70],
                               scramble="U2 F' D2 B' L2 D2 L2 B2 L2 B L U F2 L' F U2 L2 B2 D2 Fw Uw'",
                               datetime=datetime(2019, 9, 1, 11, 52, 17))
        self.assertEqual(actual, expected)

    def test_is_bad_4(self):
        input_str = "2. DNF(30.67)=9.02+21.65   B2 U2 F2 D L2 B2 U' L2 R2 B2 R' D2 F' R' U' F R B R' D2   @2019-08-28 21:42:36 "
        extractor = Extractor(total_threshold=35.0, multiphases_threshold_list=[10.0, 22.0])
        solve_result = extractor.extract(input_str)
        actutal = extractor.is_bad_solve(solve_result)
        self.assertFalse(actutal)

    def test_pickup_result_from_lines_1(self):
        tmp_input_str = """
        csTimerによって 2019-08-29 に生成 (2019-08-28 21:41:19 から 2019-08-28 21:58:54 までのソルブ)
        ソルブ数/合計: 7/16
        
        single
        ベスト: 25.49
        ワースト: 43.57

        mean of 3
        現在: DNF (σ = 0.00)
        ベスト: 28.50 (σ = 2.69)

        avg of 5
        現在: DNF (σ = 0.00)
        ベスト: 34.52 (σ = 7.87)

        avg of 12
        現在: DNF (σ = 17.62)
        ベスト: DNF (σ = 0.00)

        Average: DNF (σ = 16.94)
        Mean: 31.20

        タイム一覧:
        1. DNF(37.48)=14.53+22.95   D F2 R2 U' R2 B2 R2 U' R2 L B2 D' U L B F' D B' U'   @2019-08-28 21:41:19 
        2. DNF(30.67)=9.02+21.65   B2 U2 F2 D L2 B2 U' L2 R2 B2 R' D2 F' R' U' F R B R' D2   @2019-08-28 21:42:36 
        3. 33.78=9.58+24.19   U B2 D2 F2 U' L2 B2 F2 L' D' U2 R D U B2 F U' F'   @2019-08-28 21:44:18
        """[:-1]

        input_lines = textwrap.dedent(tmp_input_str).split('\n')
        extractor = Extractor(total_threshold=35.0, multiphases_threshold_list=[10.0, 22.0])
        actual = extractor.pickup_result_from_lines(input_lines)
        expected = [
            SolveResult(is_dnf=True,
                        total_sec=37.48,
                        multiphases=[14.53, 22.95],
                        scramble="D F2 R2 U' R2 B2 R2 U' R2 L B2 D' U L B F' D B' U'",
                        datetime=datetime(2019, 8, 28, 21, 41, 19)),
            SolveResult(is_dnf=False,
                        total_sec=33.78,
                        multiphases=[9.58, 24.19],
                        scramble="U B2 D2 F2 U' L2 B2 F2 L' D' U2 R D U B2 F U' F'",
                        datetime=datetime(2019, 8, 28, 21, 44, 18)),
        ]
        self.assertEqual(actual, expected)