def bytes_to_human_readable(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            break
        size //= 1024
    return f"{size:.2f} {unit}"
