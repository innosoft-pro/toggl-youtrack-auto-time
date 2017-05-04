#!/usr/bin/env bash
docker build --tag 't-y:latest' .
docker run -v $(pwd)/configs:/app/configs t-y:latest ./toggl_youtrack.py --track --format --since_last
