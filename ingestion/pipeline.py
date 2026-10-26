import dlt 


def main():
    pipeline = dlt.pipeline(
        pipeline_name="toystore",
        destination=dlt.destinations.duckdb("data/toystore.duckdb"),
        dataset_name="raw",
    )