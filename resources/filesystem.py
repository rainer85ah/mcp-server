import aiofiles
import aiofiles.os
from pathlib import Path
from typing import List, Optional, Any
from apps.mcp.app.core.logger import logger
from apps.mcp.app.main import mcp
from apps.mcp.app.resources.base import DataSource


@mcp.resource()
class FileSystem(DataSource):

    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()

        if not self.base_path.is_dir():
            raise ValueError(f"Base path '{self.base_path}' is not a valid directory")

    async def read(self, filepath: str, **kwargs) -> bytes:
        """
        Asynchronously read a file as bytes.

        Args:
            filepath: Relative or absolute path to the file to read.

        Returns:
            Bytes content of the file.

        Raises:
            FileNotFoundError if file does not exist.
            IsADirectoryError if the path is a directory.
            OSError for other IO errors.
        """
        full_path = Path(filepath)

        if not full_path.is_absolute():
            full_path = self.base_path / full_path

        full_path = full_path.resolve()

        # Prevent path traversal outside base_path
        if self.base_path not in full_path.parents and full_path != self.base_path:
            raise ValueError("Access outside base_path is not allowed")

        try:
            async with aiofiles.open(full_path, 'rb') as f:
                return await f.read()
        except Exception as e:
            logger.error(f"Failed to read file '{full_path}': {e}")
            raise

    async def write(self, key: str, data: Any, **kwargs) -> None:
        """
        Asynchronously write data to a file at the given relative key path.

        Args:
            key: Relative path (from base_path) where the data will be written.
            data: Data to write (must be bytes-like or string).
            kwargs: Optional keyword args like mode ('wb' or 'w') and encoding.

        Raises:
            ValueError: If writing outside base_path or unsupported data type.
            OSError: For filesystem-related errors.
        """
        full_path = (self.base_path / key).resolve()
        if self.base_path not in full_path.parents and full_path != self.base_path:
            raise ValueError("Access outside base_path is not allowed")

        mode = kwargs.get("mode", "wb")  # default: binary write
        encoding = kwargs.get("encoding", "utf-8") if 'b' not in mode else None

        # Ensure the parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, str) and 'b' not in mode:
            async with aiofiles.open(full_path, mode, encoding) as f:
                await f.write(data)
        elif isinstance(data, (bytes, bytearray)) and 'b' in mode:
            async with aiofiles.open(full_path, mode) as f:
                await f.write(data)
        else:
            raise ValueError("Unsupported data type for write. Use str or bytes.")

    async def exists(self, path: str) -> bool:
        full_path = (self.base_path / path).resolve()

        if self.base_path not in full_path.parents and full_path != self.base_path:
            logger.error(f"Access outside '{full_path}' is not allowed.")
            raise ValueError("Access outside base_path is not allowed")

        return await aiofiles.os.path.exists(full_path)

    async def is_file(self, path: str) -> bool:
        full_path = (self.base_path / path).resolve()
        if self.base_path not in full_path.parents and full_path != self.base_path:
            raise ValueError("Access outside base_path is not allowed")
        return await aiofiles.os.path.isfile(full_path)

    async def is_dir(self, path: str) -> bool:
        full_path = (self.base_path / path).resolve()
        if self.base_path not in full_path.parents and full_path != self.base_path:
            raise ValueError("Access outside base_path is not allowed")
        return await aiofiles.os.path.isdir(full_path)

    async def move(self, src: str, dest: str) -> None:
        src_path = (self.base_path / src).resolve()
        dest_path = (self.base_path / dest).resolve()
        for p in (src_path, dest_path):
            if self.base_path not in p.parents and p != self.base_path:
                raise ValueError("Access outside base_path is not allowed")

        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        await aiofiles.os.rename(src_path, dest_path)

    async def list_files(self, subfolder: Optional[str] = '') -> List[str]:
        """
        Asynchronously list files in a subfolder relative to base_path.

        Args:
            subfolder: Optional subdirectory inside base_path.

        Returns:
            List of filenames (str) in the directory.

        Raises:
            FileNotFoundError if folder does not exist.
            NotADirectoryError if path is not a directory.
            OSError for other IO errors.
        """
        folder_path = (self.base_path / subfolder).resolve()

        # Prevent directory traversal outside base_path
        if self.base_path not in folder_path.parents and folder_path != self.base_path:
            raise ValueError("Access outside base_path is not allowed")

        if not folder_path.exists():
            raise FileNotFoundError(f"Directory '{folder_path}' does not exist")

        if not folder_path.is_dir():
            raise NotADirectoryError(f"Path '{folder_path}' is not a directory")

        try:
            return await aiofiles.os.listdir(folder_path)
        except Exception as e:
            logger.error(f"Failed to list directory '{folder_path}': {e}")
            raise

