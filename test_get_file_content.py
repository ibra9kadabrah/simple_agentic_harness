import unittest
from functions.get_file_content import get_file_content
from config import MAX_CHAR

class TestGetFilesInfo(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def test_trunc(self):
        call = get_file_content("calculator", "lorem.txt")
        print("running trncated test")
        
        self.assertGreaterEqual(len(call), MAX_CHAR)
        self.assertIn("truncated", call)
        print(call)   

    def test_main(self):
        call = get_file_content("calculator", "main.py")
        print("running main.py test")

        self.assertLessEqual(len(call), MAX_CHAR)
        print(call)


    def test_calculator(self):
        call = get_file_content("calculator", "pkg/calculator.py")
        print("running calculator.py test")

        self.assertLessEqual(len(call), MAX_CHAR)
        print(call)
    
    def test_string_error_backslash(self):
        call = get_file_content("calculator", "/bin/cat")
        print("running / test")

        self.assertIn("Error: Cannot read", call)
        print(call)

    def test_string_error_file(self):
        call = get_file_content("calculator", "pkg/does_not_exist.py")
        print("running non-existent file test")

        self.assertIn("Error: File not found", call)
        print(call)


if __name__ == "__main__":
    unittest.main()