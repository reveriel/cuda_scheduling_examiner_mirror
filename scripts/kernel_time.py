# print kernel time for each launched kernel

import json



import glob
import json
import numpy
import sys

def benchmark_sort_key(benchmark):
    """Returns the key that may be used to sort benchmarks by label."""
    if not "label" in benchmark:
        return ""
    return benchmark["label"]


def print_scenario(benchmarks, name):
    """Takes a list of parsed benchmark results and a scenario name and
    print time for each benchmark"""
    # Remember, the first entry in the times array is an empty object.

    benchmarks = sorted(benchmarks, key = benchmark_sort_key)
    for benchmark in benchmarks:
        block_times = benchmark["times"][2]["block_times"] # list of floats
        it = iter(block_times)
        for start in it:
            end = next(it)

            print("%s , %.3f " % (benchmark["label"], float(end) - float(start)))

def print_kernel_times(filenames):
    parsed_files = []
    for name in filenames:
        with open(name) as f:
            parsed_files.append(json.loads(f.read()))
        # Group the files by scenario
    scenarios = {}
    for benchmark in parsed_files:
        scenario = benchmark["scenario_name"]
        if not scenario in scenarios:
            scenarios[scenario] = []
        scenarios[scenario].append(benchmark)

    for scenario in scenarios:
        print_scenario(scenarios[scenario], scenario)


if __name__ == "__main__":
    base_directory = "./results"
    if len(sys.argv) > 2:
        print "Usage: python %s [directory containing results (./results)]" % (
            sys.argv[0])
        exit(1)
    if len(sys.argv) == 2:
        base_directory = sys.argv[1]
    filenames = glob.glob(base_directory + "/*.json")
    print_kernel_times(filenames)
