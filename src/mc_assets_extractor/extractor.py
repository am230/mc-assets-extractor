from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import Callable, TypedDict
import json

from mc_assets_extractor.helper import bytes_to_human_readable


class AssetObject(TypedDict):
    hash: str
    size: int


class AssetIndex(TypedDict):
    objects: dict[str, AssetObject]


def hash_to_path(hash: str) -> Path:
    return Path(hash[:2]) / hash


@dataclass(slots=True, eq=True)
class ExtractProgress:
    total_bytes: int
    processed_bytes: int
    total_objects: int
    processed_objects: int
    current_object: str | None = None

    def __str__(self) -> str:
        processed_bytes_str = bytes_to_human_readable(self.processed_bytes)
        total_bytes_str = bytes_to_human_readable(self.total_bytes)
        return (
            f"Processed {self.processed_objects}/{self.total_objects} objects, ({self.current_object})\n"
            f"{processed_bytes_str}/{total_bytes_str} ({self.processed_bytes/self.total_bytes*100:.2f}%)"
        )


def extract_assets(
    index_path: Path,
    objects_path: Path,
    output_path: Path,
    progress_callback: Callable[[ExtractProgress], None],
) -> None:
    asset_index = AssetIndex(**json.loads(index_path.read_text(encoding="utf-8")))
    total_objects = len(asset_index["objects"])
    total_bytes = sum(obj["size"] for obj in asset_index["objects"].values())
    progress = ExtractProgress(
        total_bytes=total_bytes,
        processed_bytes=0,
        total_objects=total_objects,
        processed_objects=0,
    )

    for key, value in asset_index["objects"].items():
        asset_object = AssetObject(**value)
        hash = asset_object["hash"]
        size = asset_object["size"]
        object_path = objects_path / hash_to_path(hash)
        output_object_path = output_path / key
        output_object_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(object_path, output_object_path)

        progress.processed_bytes += size
        progress.processed_objects += 1
        progress.current_object = key
        progress_callback(progress)
