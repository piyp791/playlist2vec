import unittest

from scale import get_scale

# Constants for scaling logic
REQUEST_CAPACITY = {
    '/search-random': 25,
    '/search': 25,
    '/populate': 70,
}
MAX_REPLICAS_PER_SERVICE = {
    'playlist2vec_stack_search-service': 4,
    'playlist2vec_stack_autocomplete-service': 3,
}

ENDPOINTS_SERVICES = {
    '/search-random' : 'playlist2vec_stack_search-service',
    '/search' : 'playlist2vec_stack_search-service',
    '/populate' : 'playlist2vec_stack_autocomplete-service'
}


class TestGetScale(unittest.TestCase):

    def test_no_requests(self):
        request_counts = {
            '/search-random': 0,
            '/search': 0,
            '/populate': 0,
        }
        expected_replicas = {
            'playlist2vec_stack_search-service': 1,
            'playlist2vec_stack_autocomplete-service': 1,
        }
        result = get_scale(request_counts)
        self.assertEqual(result, expected_replicas)

    
    def test_requests_within_capacity(self):
        request_counts = {
            '/search-random': 900,
            '/search': 2400,
            '/populate': 600,
        }
        expected_replicas = {
            'playlist2vec_stack_search-service': 3,
            'playlist2vec_stack_autocomplete-service': 1,
        }
        result = get_scale(request_counts)
        self.assertEqual(result, expected_replicas)

    
    def test_exceeding_max_replicas(self):
        request_counts = {
            '/search-random': 6000,
            '/search': 6000,
            '/populate': 30000,
        }
        expected_replicas = {
            'playlist2vec_stack_search-service': 4,
            'playlist2vec_stack_autocomplete-service': 3,
        }
        result = get_scale(request_counts)
        self.assertEqual(result, expected_replicas)

    
    def test_partial_requests(self):
        request_counts = {
            '/search-random': 30,
            '/search': 600,
            '/populate': 0,
        }
        expected_replicas = {
            'playlist2vec_stack_search-service': 1,
            'playlist2vec_stack_autocomplete-service': 1,
        }
        result = get_scale(request_counts)
        self.assertEqual(result, expected_replicas)
        
if __name__ == "__main__":
    unittest.main()