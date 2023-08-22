import pytest
from checkers import checkout, getout
import random
import string
import yaml
from datetime import datetime
from pathlib import Path

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    file_path = Path(data.get("folder_in"))
    if not file_path.exists():
        return checkout(f'mkdir {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")} {data.get("folder_ext2")}', "")


@pytest.fixture()
def clear_folders():
    return checkout(f'rm -rf {data.get("folder_in")}/* {data.get("folder_out")}/* {data.get("folder_ext")}/* {data.get("folder_ext2")}/*', "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data.get("count")):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f'cd {data.get("folder_in")}; dd if=/dev/urandom of={filename} bs={data.get("bs")} count=1 iflag=fullblock', ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout(f'cd {data.get("folder_in")}; mkdir {subfoldername}', ""):
        return None, None
    if not checkout(
            f'cd {data.get("folder_in")}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs=1M count=1 iflag=fullblock', ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%S.%f")}')
    yield
    print(f'Finish: {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture()
def make_bad_arx():
    checkout(f'cd {data.get("folder_in")}; 7z a {data.get("folder_out")}/arxbad -t{data.get("type")}', "Everything is Ok")
    checkout(f'truncate -s 1 {data.get("folder_out")}/arxbad.{data.get("type")}', "Everything is Ok")
    yield "arxbad"
    checkout(f'rm -f {data.get("folder_out")}/arxbad.{data.get("type")}', "")


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"),
                                                                            data["count"], data["bs"], stat), "")
