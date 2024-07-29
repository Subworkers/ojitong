import json
import jsonlines
from datetime import datetime
from pathlib import Path
from data import DATA_BASE_PATH
from data.const import PostType, DataType

RESOURCES_PATH = Path(DATA_BASE_PATH***REMOVED*** / "bench"

def save_bench_data_jsonl_by_types(post_type: PostType, data_type: DataType, samples: list***REMOVED***:
    filename = set_filename_by_data_type(data_type***REMOVED***
    file_path = RESOURCES_PATH / post_type.value / filename
    write_samples_by_line(file_path, samples***REMOVED***

def set_filename_by_data_type(data_type: DataType***REMOVED***:
    filename = f"{data_type.value***REMOVED***.jsonl"
    return filename

def write_samples_by_line(file_path, samples: list***REMOVED***:
    with open(file_path, "w", encoding="utf-8"***REMOVED*** as f:
        for data in samples:
            json.dump(data, f, ensure_ascii=False***REMOVED***
            f.write("\n"***REMOVED***

def read_samples_by_line(file***REMOVED***:
    file_path = str(RESOURCES_PATH.joinpath(file***REMOVED******REMOVED***
    with jsonlines.open(file_path***REMOVED*** as f:
        for line in f.iter(***REMOVED***:
            yield json.loads(line***REMOVED***

def generate_s3_path(
    bucket_name="ojitong",
    deploy_phase="local",
    prefix="news_data",
    extension=".csv",
    today_datetime: datetime=datetime.today(***REMOVED***
***REMOVED***:
    timestamp = today_datetime.strftime("%Y%m%d_%H%M%S"***REMOVED***
    return f"s3://{bucket_name***REMOVED***/{deploy_phase***REMOVED***/{prefix***REMOVED***/{timestamp***REMOVED***{extension***REMOVED***"