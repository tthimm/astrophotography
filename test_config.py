import unittest
import config

class TestConfigFunctions(unittest.TestCase):

    def test_read_config(self):
        self.assertIn('VideoResolution', config.read_config())
        self.assertIn('ImageResolution', config.read_config())
        self.assertIn('PreviewResolution', config.read_config())
        self.assertIn('VideoTimer', config.read_config())
    
    def test_split_config_entry(self):
        self.assertEqual((1920, 1080), config.split_config_entry('1920x1080'))

if __name__ == '__main__':
    unittest.main()