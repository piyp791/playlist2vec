import subprocess
import os
from datetime import datetime

TIMEFRAME = 60  # seconds

LOG_FILE_PARSER = '/home/ubuntu/playlist2vec/autoscale/get_requests.sh'

SEARCH_SERVICE = 'playlist2vec_stack_search-service'
AUTOCOMPLETE_SERVICE = 'playlist2vec_stack_autocomplete-service' 

# Constants for scaling logic
SERVICE_INSTANCE_CAPACITY = {
    SEARCH_SERVICE: 25,
    AUTOCOMPLETE_SERVICE: 70,
}

MAX_REPLICAS_PER_SERVICE = {
    SEARCH_SERVICE: 4,
    AUTOCOMPLETE_SERVICE: 3,
}

ENDPOINTS_SERVICES = {
    '/search-random' : SEARCH_SERVICE,
    '/search' : SEARCH_SERVICE,
    '/populate' : AUTOCOMPLETE_SERVICE
}

def get_current_replicas(service_name):
    # Run the Docker command to get service details
    command = f"docker service inspect {service_name} --format '{{{{.Spec.Mode.Replicated.Replicas}}}}'"
    result = os.popen(command).read().strip()  # Use os.popen to capture the output

    if result.isdigit():
        return int(result)  # Convert the result to an integer
    else:
        print("Error: Unable to retrieve replicas.")
        return None

def get_scale(request_counts):
    required_service_replicas = {SEARCH_SERVICE: 1, AUTOCOMPLETE_SERVICE: 1}
    service_requests_count = {}

    for endpoint, count in request_counts.items():
        avg_count = count // TIMEFRAME
        print(f"Endpoint: {endpoint}, Count: {count}, Avg Count: {avg_count}")
        service_name = ENDPOINTS_SERVICES.get(endpoint, None)
        service_requests_count[service_name] = service_requests_count.get(service_name, 0) + avg_count

    print(f"Cumulative Service Requests Count: {service_requests_count}")

    for service, avg_count in service_requests_count.items():
        capacity = SERVICE_INSTANCE_CAPACITY.get(service, 1)
        desired_replicas = (avg_count + capacity - 1) // capacity
        
        required_service_replicas[service] = max(min(desired_replicas, MAX_REPLICAS_PER_SERVICE[service]), 1)
    return required_service_replicas

def main():
    print(f"Reading request counts from the Bash script at time: {datetime.now()}")
    # Call the Bash function and capture its output
    result = subprocess.run(['bash', LOG_FILE_PARSER], capture_output=True, text=True)
    print("Done...")
    output = result.stdout.strip().splitlines()

    # Parse the output into a dictionary
    request_counts = {}
    for line in output:
        key, value = line.split('=')
        request_counts[key] = int(value)

    # Scale services based on the request counts
    required_service_replicas = get_scale(request_counts)
    print(f"Required Service Replicas: {required_service_replicas}")
    # Execute scaling commands
    for service, replicas in required_service_replicas.items():
        
        current_replicas = get_current_replicas(service)
        if current_replicas == replicas:
            print(f"{service} is already at {replicas} replicas")
            continue
        
        print(f"Scaling {service} to {replicas} replicas")
        os.system(f"docker service scale {service}={replicas}")

if __name__ == "__main__":
    main()
