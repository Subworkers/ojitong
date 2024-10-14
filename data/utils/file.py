import json
import jsonlines
from datetime import datetime
from pathlib import Path
from data import DATA_BASE_PATH
from data.const import PostType, DataType

RESOURCES_PATH = Path(DATA_BASE_PATH) / "bench"

def save_bench_data_jsonl_by_types(post_type: PostType, data_type: DataType, samples: list):
    filename = set_filename_by_data_type(data_type)
    file_path = RESOURCES_PATH / post_type.value / filename
    write_samples_by_line(file_path, samples)

def set_filename_by_data_type(data_type: DataType):
    filename = f"{data_type.value}.jsonl"
    return filename

def write_samples_by_line(file_path, samples: list):
    with open(file_path, "w", encoding="utf-8") as f:
        for data in samples:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

def read_samples_by_line(file):
    file_path = str(RESOURCES_PATH.joinpath(file))
    with jsonlines.open(file_path) as f:
        for line in f.iter():
            yield json.loads(line)

def generate_s3_path(
    bucket_name="ojitong",
    deploy_phase="local",
    prefix="news_data",
    extension=".csv",
    today_datetime: datetime=datetime.today()
):
    timestamp = today_datetime.strftime("%Y%m%d_%H%M%S")
    return f"s3://{bucket_name}/{deploy_phase}/{prefix}/{timestamp}{extension}"