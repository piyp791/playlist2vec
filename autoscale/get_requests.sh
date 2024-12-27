#!/bin/bash

# Configuration
LOG_FILE="/var/log/nginx/access.log"  # Path to the Nginx access log file
TIMEFRAME=60 # Timeframe in seconds

read_logs() {
    local start end
    local search_random_count=0
    local search_count=0
    local populate_count=0

    start=$(date -d '1 minute ago' '+[%d/%b/%Y:%H:%M:%S]')
    end=$(date '+[%d/%b/%Y:%H:%M:%S]')

    # Use awk to process the log file
    awk -v start="$start" -v end="$end" -v search_random_count="$search_random_count" -v search_count="$search_count" -v populate_count="$populate_count" '
        BEGIN {
            # Initialize counts
            search_random_count = 0
            search_count = 0
            populate_count = 0
        }
        $4 >= start && $4 <= end {
            if ($7 ~ /\/search-random/) {
                search_random_count++
            } else if ($7 ~ /\/search/) {
                search_count++
            } else if ($7 ~ /\/populate/) {
                populate_count++
            }
        } 
        END { 
            print "/search-random=" search_random_count;
            print "/search=" search_count;
            print "/populate=" populate_count;
        }' /var/log/nginx/access.log
}

read_logs


