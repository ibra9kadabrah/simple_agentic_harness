import unittest
from functions.run_python_file import run_python_file

class TestRunPythonFile(unittest.TestCase):    
    def setUp(self):
        return super().setUp()
    
    def test_print_usage(self):
        call = run_python_file("calculator", "main.py")
        print(call)

    def test_calculation(self):
        call = run_python_file("calculator", "main.py", ["3 + 5"])
        print(call)
        
    def test_run_tests(self):
        call = run_python_file("calculator", "tests.py")
        print(call)
    
    def test_run_err(self):
        call = run_python_file("calculator", "../main.py")
        print(call)

        self.assertIn("Error", call)

    def test_run_err1(self):
        call = run_python_file("calculator", "nonexistent.py")
        print(call)

        self.assertIn("Error", call)

    def test_run_err2(self):
        call = run_python_file("calculator", "lorem.txt")
        print(call)

        self.assertIn("Error", call)


if __name__ == "__main__":
    unittest.main()