from dataclasses import dataclass
from pathlib import Path
import sys


def get_minecraft_dir() -> Path:
    system = sys.platform
    if system == "win32":
        return Path.home() / "AppData" / "Roaming" / ".minecraft"
    elif system == "darwin":
        return Path.home() / "Library" / "Application Support" / "minecraft"
    elif system == "linux":
        return Path.home() / ".minecraft"
    else:
        raise Exception("Unsupported system")


@dataclass(frozen=True, slots=True, eq=True)
class AssetsDir:
    assets: Path

    @property
    def indexes(self) -> Path:
        return self.assets / "indexes"

    @property
    def objects(self) -> Path:
        return self.assets / "objects"

    def get_latest_index(self) -> Path:
        asset_index_entries = list(self.indexes.glob("*.json"))
        if len(asset_index_entries) == 0:
            raise FileNotFoundError("No asset index found")

        def get_stem_as_int(x: Path) -> int:
            return int(x.stem) if x.stem.isdigit() else -1

        sorted_index_entries = sorted(asset_index_entries, key=get_stem_as_int)
        return sorted_index_entries[-1]


@dataclass(frozen=True, slots=True, eq=True)
class MinecraftDir:
    mcdir: Path

    @classmethod
    def from_path(cls, path: Path) -> "MinecraftDir":
        return cls(mcdir=path)

    @classmethod
    def from_default(cls) -> "MinecraftDir":
        return cls(mcdir=get_minecraft_dir())

    @property
    def assets(self) -> AssetsDir:
        return AssetsDir(self.mcdir / "assets")
