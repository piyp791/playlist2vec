import subprocess
import os
from datetime import datetime
from log_setup import setup_logging

current_dir = '/home/peps/research/playlist2vec/autoscale'
logger = setup_logging(f'{current_dir}/logs')

class ScaleServices:
    def __init__(self):
        # Constants for the autoscaling logic
        self.TIMEFRAME = 60  # time in seconds after which the script will be run
        self.LOG_FILE_PARSER = f'{current_dir}/get_requests.sh'

        self.SEARCH_SERVICE = 'playlist2vec_stack_search-service'
        self.AUTOCOMPLETE_SERVICE = 'playlist2vec_stack_autocomplete-service' 

        self.SERVICE_INSTANCE_CAPACITY = {
            self.SEARCH_SERVICE: 25,
            self.AUTOCOMPLETE_SERVICE: 70,
        }

        self.MAX_REPLICAS_PER_SERVICE = {
            self.SEARCH_SERVICE: 4,
            self.AUTOCOMPLETE_SERVICE: 3,
        }

        self.ENDPOINTS_SERVICES = {
            '/search-random' : self.SEARCH_SERVICE,
            '/search' : self.SEARCH_SERVICE,
            '/populate' : self.AUTOCOMPLETE_SERVICE
        }
        
    def __read_log_parser_output(self):
        logger.info(f"Reading request counts from the Bash script at: {datetime.now()}")
        result = subprocess.run(['bash', self.LOG_FILE_PARSER], capture_output=True, text=True)
        logger.info("Done...")
        # capture error if any
        if result.returncode != 0:
            logger.error(f"Error: {result.stderr}")
            return None
        
        output = result.stdout.strip().splitlines()

        # Parse the output into a dictionary
        request_counts = {}
        for line in output:
            key, value = line.split('=')
            request_counts[key] = int(value)
        return request_counts

    def __get_current_replicas(self, service_name):
        # Run the Docker command to get service details
        command = f"docker service inspect {service_name} --format '{{{{.Spec.Mode.Replicated.Replicas}}}}'"
        result = os.popen(command).read().strip()  # Use os.popen to capture the output

        if result.isdigit():
            return int(result)  # Convert the result to an integer
        else:
            logger.error("Error: Unable to retrieve replicas.")
            return None

    def get_scale(self, request_counts):
        required_service_replicas = {self.SEARCH_SERVICE: 1, self.AUTOCOMPLETE_SERVICE: 1}
        service_requests_count = {}

        for endpoint, count in request_counts.items():
            avg_count = count // self.TIMEFRAME
            logger.info(f"Endpoint: {endpoint}, Count: {count}, Avg Count: {avg_count}")
            service_name = self.ENDPOINTS_SERVICES.get(endpoint, None)
            service_requests_count[service_name] = service_requests_count.get(service_name, 0) + avg_count

        logger.info(f"Cumulative Service Requests Count: {service_requests_count}")

        for service, avg_count in service_requests_count.items():
            capacity = self.SERVICE_INSTANCE_CAPACITY.get(service, 1)
            desired_replicas = (avg_count + capacity - 1) // capacity
            
            required_service_replicas[service] = max(min(desired_replicas, self.MAX_REPLICAS_PER_SERVICE[service]), 1)
        return required_service_replicas
    
    def do_scale(self):
        # Read request counts from the Bash script
        request_counts = self.__read_log_parser_output()
        if request_counts is None:
            logger.error("Error reading request counts. Exiting.")
            return

        required_service_replicas = self.get_scale(request_counts)
        logger.info(f"Required Service Replicas: {required_service_replicas}")
        # Execute scaling commands
        for service, replicas in required_service_replicas.items():
            current_replicas = self.__get_current_replicas(service)
            if current_replicas == replicas:
                logger.info(f"{service} is already at {replicas} replicas")
                continue
            
            logger.info(f"Scaling {service} to {replicas} replicas")
            os.system(f"docker service scale {service}={replicas}")
            

if __name__ == "__main__":
    scale_services = ScaleServices()
    scale_services.do_scale()
