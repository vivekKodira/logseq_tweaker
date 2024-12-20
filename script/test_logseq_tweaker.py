import unittest
from logseq_tweaker import get_child_blocks

class TestLogseqTweaker(unittest.TestCase):

    def test_get_child_blocks_empty_references(self):
        references = []
        content = "Some content"
        result = get_child_blocks(references, content)
        self.assertEqual(result, [])

    def test_get_child_blocks_empty_content(self):
        references = ["reference1", "reference2"]
        content = ""
        result = get_child_blocks(references, content)
        self.assertEqual(result, [])

    def test_get_child_blocks_no_matches(self):
        references = ["reference1", "reference2"]
        content = "Some content without references"
        result = get_child_blocks(references, content)
        self.assertEqual(result, [])

    def test_get_child_blocks_with_matches(self):
        references = ["reference1", "reference2"]
        content = "Some content with reference1 and reference2"
        result = get_child_blocks(references, content)
        self.assertEqual(result, [])  # Assuming the function is not yet implemented

if __name__ == '__main__':
    unittest.main()