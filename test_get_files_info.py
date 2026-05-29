import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def setUp(self):
        return super().setUp()
    
    def _check_multiline(self, call):
        contains_py = ".py" in call
        contains_size = "file_size" in call
        contains_dir_bool = "is_dir" in call
        if contains_py and contains_size and contains_dir_bool:
            return True
        return False

    def test_Calculator_dir(self):
        call = get_files_info("calculator", ".")
        print("Result for current directory")
        print(call)

        result = self._check_multiline(call)
        self.assertTrue(result)

    def test_Calculator_subdirectory(self):
        call = get_files_info("calculator", "pkg")
        print("Result for current directory")
        print(call)

        result = self._check_multiline(call)
        self.assertTrue(result)

    def test_Calculator_bin(self):
        call = get_files_info("calculator", "/bin")
        print("Result for current directory")
        print(call)

        self.assertIn("Error:", call)
        self.assertIn("/bin", call)
    
    def test_Calculator_backtracking(self):
        call = get_files_info("calculator","../")
        print("Result for current directory")
        print(call)

        self.assertIn("Error", call)
        self.assertIn("../", call)

if __name__ == "__main__":
    unittest.main()