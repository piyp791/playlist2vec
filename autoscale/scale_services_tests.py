import unittest
from scale_services import ScaleServices

class TestScaleServices(unittest.TestCase):
    
    def setUp(self):
        self.scale_services = ScaleServices()

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
            '/search-random': 900,
            '/search': 2400,
            '/populate': 600,
        }
        expected_replicas = {
            self.scale_services.SEARCH_SERVICE: 3,
            self.scale_services.AUTOCOMPLETE_SERVICE: 1,
        }
        result = self.scale_services.get_scale(request_counts)
        self.assertEqual(result, expected_replicas)

    
    def test_exceeding_max_replicas(self):
        request_counts = {
            '/search-random': 6000,
            '/search': 6000,
            '/populate': 30000,
        }
        expected_replicas = {
            self.scale_services.SEARCH_SERVICE: 4,
            self.scale_services.AUTOCOMPLETE_SERVICE: 3,
        }
        result = self.scale_services.get_scale(request_counts)
        self.assertEqual(result, expected_replicas)

    
    def test_partial_requests(self):
        request_counts = {
            '/search-random': 30,
            '/search': 600,
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