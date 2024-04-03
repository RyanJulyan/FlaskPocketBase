import os
from typing import List


def list_folders(directory: str) -> List[str]:
    return [
        d
        for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d))
    ]
