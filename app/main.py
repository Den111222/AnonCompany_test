"""Main file."""

import asyncio
import hashlib
import logging
import tempfile
from pathlib import Path

import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')   # noqa: WPS323

REPO_URL = (
    'https://gitea.radium.group/api/v1/repos/radium/' +
    'project-configuration/git/trees/master?recursive=1'
)
BASE_URL = (
    'https://gitea.radium.group/radium/project-configuration/' +
    'raw/branch/master'
)
NUM_TASKS = 3
CHUNK_SIZE = 1024
SHA256_BUFFER_SIZE = 4096


async def fetch_file_list(session: aiohttp.ClientSession) -> list[str]:
    """Fetch the list of files from the repository.

    Args:
        session: An aiohttp ClientSession object for making HTTP requests.

    Returns:
        A list of file paths.
    """
    async with session.get(REPO_URL) as response:
        response.raise_for_status()
        resp_data = await response.json()
        return [
            each_file['path']
            for each_file in resp_data['tree']
            if each_file['type'] == 'blob'
        ]


async def download_file(
    session: aiohttp.ClientSession, url: str, dest: Path,
) -> None:
    """Download a file from a URL to a local destination.

    Args:
        session: An aiohttp ClientSession object for making HTTP requests.
        url: The URL of the file to download.
        dest: The local path where the file should be saved.
    """
    async with session.get(url) as response:
        response.raise_for_status()
        with dest.open('wb') as local_file:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                local_file.write(chunk)


async def download_files(
    session: aiohttp.ClientSession,
    files: list[str],
    base_url: str,
    dest_dir: Path,
) -> None:
    """Download multiple files concurrently.

    Args:
        session: An aiohttp ClientSession object for making HTTP requests.
        files: A list of file paths to download.
        base_url: The base URL for the file downloads.
        dest_dir: The directory where the files should be saved.
    """
    tasks = []
    for path in files:
        url = '{base_url}/{path}'.format(base_url=base_url, path=path)
        dest = dest_dir / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        tasks.append(download_file(session, url, dest))
    await asyncio.gather(*tasks)


def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file.

    Args:
        file_path: The path to the file.

    Returns:
        The SHA-256 hash of the file as a hexadecimal string.
    """
    sha256 = hashlib.sha256()
    with file_path.open('rb') as opened_file:
        while True:
            chunk = opened_file.read(SHA256_BUFFER_SIZE)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


async def process_files(file_paths: list[Path]) -> None:
    """Process files to calculate their SHA-256 hashes and print the results.

    Args:
        file_paths: A list of file paths to process.
    """
    tasks = [asyncio.to_thread(calculate_sha256, path) for path in file_paths]
    hashes = await asyncio.gather(*tasks)
    for path, hash_value in zip(file_paths, hashes):
        logging.info('{path}: {hash_value}'.format(
            path=path, hash_value=hash_value,
        ))


def split_list(                                                 # noqa: WPS210
    input_list: list[str], num_chunks: int,
) -> list[list[str]]:
    """Split a list into approximately equal-sized chunks.

    Args:
        input_list: The list to split.
        num_chunks: The number of chunks to create.

    Returns:
        A list of chunks, where each chunk is a list of
        items from the original list.
    """
    avg_chunk_size = len(input_list) // num_chunks
    remainder = len(input_list) % num_chunks
    chunks = []
    start = 0
    for chunk_index in range(num_chunks):
        end = start + avg_chunk_size
        if chunk_index < remainder:
            end += 1
        chunks.append(input_list[start:end])
        start = end
    return chunks


async def main() -> None:                                       # noqa: WPS210
    """Coordinate file download and processing."""
    async with aiohttp.ClientSession() as session:
        file_list = await fetch_file_list(session)

        chunks = split_list(file_list, NUM_TASKS)

        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_dir = Path(tmpdirname)
            base_raw_url = BASE_URL

            download_tasks = [
                download_files(session, chunk, base_raw_url, temp_dir)
                for chunk in chunks
            ]
            await asyncio.gather(*download_tasks)

            all_file_paths = [temp_dir / file_path for file_path in file_list]
            await process_files(all_file_paths)


if __name__ == '__main__':
    asyncio.run(main())                                 # pragma no cover
