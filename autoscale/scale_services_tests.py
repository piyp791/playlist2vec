import json
import unittest
from scale_services import ScaleServices

class TestScaleServices(unittest.TestCase):
    
    def setUp(self):
        current_dir = '/home/peps/research/playlist2vec/autoscale'
        
        with open(f'{current_dir}/config.json', 'r') as f:
            self.config = json.load(f)
            self.scale_services = ScaleServices(self.config)

    def test_no_requests(self):
        request_counts = {
            '/search-random': 0,
            '/search': 0,
            '/populate': 0,
        }
        expected_replicas = {
            self.scale_services.SEARCH_SERVICE: 1,
            self.scale_services.AUTOCOMPLETE_SERVICE: 1,
        }
        result = self.scale_services.get_scale(request_counts)
        self.assertEqual(result, expected_replicas)

    
    def test_requests_within_capacity(self):
        request_counts = {
            '/search-random': 15 * self.config['timeframe'],
            '/search': 40 * self.config['timeframe'],
            '/populate': 10 * self.config['timeframe'],
        }
        expected_replicas = {
            self.scale_services.SEARCH_SERVICE: 3,
            self.scale_services.AUTOCOMPLETE_SERVICE: 1,
        }
        result = self.scale_services.get_scale(request_counts)
        self.assertEqual(result, expected_replicas)

    
    def test_exceeding_max_replicas(self):
        request_counts = {
            '/search-random': 100 * self.config['timeframe'],
            '/search': 100 * self.config['timeframe'],
            '/populate': 500 * self.config['timeframe'],
        }
        expected_replicas = {
            self.scale_services.SEARCH_SERVICE: 4,
            self.scale_services.AUTOCOMPLETE_SERVICE: 3,
        }
        result = self.scale_services.get_scale(request_counts)
        self.assertEqual(result, expected_replicas)

    
    def test_partial_requests(self):
        request_counts = {
            '/search-random': 15 * self.config['timeframe'],
            '/search': 10 * self.config['timeframe'],
            '/populate': 0,
        }
        expected_replicas = {
            self.scale_services.SEARCH_SERVICE: 1,
            self.scale_services.AUTOCOMPLETE_SERVICE: 1,
        }
        result = self.scale_services.get_scale(request_counts)
        self.assertEqual(result, expected_replicas)
        
if __name__ == "__main__":
    unittest.main()