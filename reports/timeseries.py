#!/usr/bin/env python3

import json
from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd
import os

# Converts nanoseconds to a rounded UTC datetime at the minute level
def convert_time(nano):
    return datetime.utcfromtimestamp(nano / 1e9).replace(second=0, microsecond=0)

def process_uptime(file_path):
    now = datetime.utcnow().replace(second=0, microsecond=0)
    window_start = now - timedelta(minutes=5)

    # Data structure to collect uptime per endpoint per minute
    endpoint_status = defaultdict(lambda: defaultdict(list))

    with open(file_path, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                for resource in entry.get("resourceMetrics", []):
                    for scope_metric in resource.get("scopeMetrics", []):
                        for metric in scope_metric.get("metrics", []):
                            if metric.get("name") != "http_req_duration":
                                continue

                            for dp in metric.get("histogram", {}).get("dataPoints", []):
                                ts = convert_time(int(dp.get("timeUnixNano")))
                                if ts < window_start:
                                    continue

                                ep_name = "unknown"
                                expected = "true"
                                status = "200"

                                for attr in dp.get("attributes", []):
                                    key = attr.get("key")
                                    val = attr.get("value", {}).get("stringValue")
                                    if key == "endpoint_name":
                                        ep_name = val
                                    elif key == "expected_response":
                                        expected = val
                                    elif key == "status":
                                        status = val

                                is_up = expected == "true" and status == "200"
                                endpoint_status[ep_name][ts].append(is_up)

            except json.JSONDecodeError:
                continue

    # Compose summary
    rows = []
    minutes = [window_start + timedelta(minutes=i) for i in range(5)]
    endpoints = sorted(endpoint_status.keys())

    for ep in endpoints:
        row = {"endpoint": ep}
        for t in minutes:
            statuses = endpoint_status[ep].get(t)
            if statuses is None:
                row[t.strftime("%H:%M")] = "NULL"
            else:
                row[t.strftime("%H:%M")] = f"{round(100 * sum(statuses)/len(statuses), 1)}%"
        rows.append(row)

    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

if __name__ == "__main__":
    file_path = os.path.expanduser("/tmp/otel-metrics.json")
    process_uptime(file_path)
