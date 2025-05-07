#!/usr/bin/env python3

import json
from collections import defaultdict
import pandas as pd
import os

def process_otel_metrics(file_path):
    # Use a defaultdict to automatically initialize stats for each endpoint
    summary = defaultdict(lambda: {
        "count": 0,              # Number of times this endpoint was hit
        "sum": 0.0,              # Total duration across all hits (ms)
        "status": None,          # Last seen HTTP status code
        "expected_response": None,  # Whether a 200-level response was expected
        "error_code": None       # Last seen error code (if any)
    })

    # Open and process each line of the OTEL JSON file (one JSON object per line)
    with open(file_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)

                # Navigate into OpenTelemetry's hierarchical structure:
                for resource in entry.get("resourceMetrics", []):
                    for scope_metric in resource.get("scopeMetrics", []):
                        for metric in scope_metric.get("metrics", []):
                            # We're only interested in request duration metrics
                            if metric.get("name") != "http_req_duration":
                                continue

                            # Each histogram dataPoint contains a summary for a time range
                            for dp in metric.get("histogram", {}).get("dataPoints", []):
                                endpoint = ""
                                status = ""
                                expected_response = ""
                                error_code = None

                                # Pull metadata from attributes array (labels)
                                for attr in dp.get("attributes", []):
                                    if attr["key"] == "endpoint_name":
                                        endpoint = attr["value"].get("stringValue", "")
                                    elif attr["key"] == "status":
                                        status = attr["value"].get("stringValue", "")
                                    elif attr["key"] == "expected_response":
                                        expected_response = attr["value"].get("stringValue", "")
                                    elif attr["key"] == "error_code":
                                        error_code = attr["value"].get("stringValue", "")

                                # Aggregate metrics per endpoint
                                if endpoint:
                                    summary[endpoint]["count"] += int(dp.get("count", 0))
                                    summary[endpoint]["sum"] += float(dp.get("sum", 0))
                                    summary[endpoint]["status"] = status
                                    summary[endpoint]["expected_response"] = expected_response
                                    if error_code:
                                        summary[endpoint]["error_code"] = error_code
            except json.JSONDecodeError:
                # Skip any lines that aren’t valid JSON
                continue

    # Transform the aggregated stats into a DataFrame for sorting and display
    rows = []
    for ep, metrics in summary.items():
        avg_duration = metrics["sum"] / metrics["count"] if metrics["count"] else 0
        rows.append({
            "endpoint": ep,
            "status": metrics["status"],
            "expected_response": metrics["expected_response"],
            "error_code": metrics["error_code"],
            "request_count": metrics["count"],
            "avg_duration_ms": round(avg_duration, 2)
        })

    # Sort results by request volume, highest first
    df = pd.DataFrame(rows).sort_values(by="request_count", ascending=False)

    # Output the summary table to stdout
    print(df.to_string(index=False))

if __name__ == "__main__":
    # Assumes metrics are written here by your OTEL Collector
    file_path = os.path.expanduser("/tmp/otel-metrics.json")
    process_otel_metrics(file_path)
