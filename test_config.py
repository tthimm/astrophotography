import unittest
import config

class TestConfigFunctions(unittest.TestCase):

    def test_read_config(self):
        self.assertIn('VideoResolution', config.read_config()[0]['Video'])
        self.assertIn('ImageResolution', config.read_config()[0]['Video'])
        self.assertIn('PreviewResolution', config.read_config()[0]['Video'])
        self.assertIn('VideoTimer', config.read_config()[0]['Video'])
        self.assertIn('Host', config.read_config()[0]['FTP'])
        self.assertIn('User', config.read_config()[0]['FTP'])
        self.assertIn('Password', config.read_config()[0]['FTP'])

        self.assertIn('VideoResolution', config.read_config()[1]['Video'])
        self.assertIn('ImageResolution', config.read_config()[1]['Video'])
        self.assertIn('PreviewResolution', config.read_config()[1]['Video'])
        self.assertIn('VideoTimer', config.read_config()[1]['Video'])
        self.assertIn('Host', config.read_config()[1]['FTP'])
        self.assertIn('User', config.read_config()[1]['FTP'])
        self.assertIn('Password', config.read_config()[1]['FTP'])
    
    def test_split_config_entry(self):
        self.assertEqual((1920, 1080), config._split_config_entry('1920x1080'))

if __name__ == '__main__':
    unittest.main()
