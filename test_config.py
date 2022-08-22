import unittest
import config

class TestConfigFunctions(unittest.TestCase):

    def test_read_config(self):
        self.assertIn('VideoResolution', config.read_config())
        self.assertIn('ImageResolution', config.read_config())
        self.assertIn('PreviewResolution', config.read_config())
        self.assertIn('VideoTimer', config.read_config())
    
    def test_split_config_entry(self):
        conf = config.read_config()
        self.assertEqual((1920, 1080), config.split_config_entry(conf['VideoResolution']))
        self.assertEqual((2592, 1944), config.split_config_entry(conf['ImageResolution']))
        self.assertEqual((800, 600), config.split_config_entry(conf['PreviewResolution']))

if __name__ == '__main__':
    unittest.main()