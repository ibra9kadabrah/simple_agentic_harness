import unittest
from functions.write_file import write_file

class TestWriteFile(unittest.TestCase):
    def setUp(self):
        return super().setUp()
    
    def test_lorem(self):
        call = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print("Testing lorem ipsum")
        print(call)

    def test_more_lorem(self):
        call = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(call)

    def test_not_allowed(self):
        call = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(call)

    
if __name__ == "__main__":
    unittest.main()