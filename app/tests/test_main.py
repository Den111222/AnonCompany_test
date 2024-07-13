"""This is test of app/main.py."""

import hashlib
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest
from aioresponses import aioresponses

from app.main import (
    calculate_sha256,
    download_files,
    fetch_file_list,
    main,
    process_files,
    split_list,
)

REPO_URL = (
    'https://gitea.radium.group/api/v1/repos/' +
    'radium/project-configuration/git/trees/master?recursive=1'
)
BASE_RAW_URL = (
    'https://gitea.radium.group/radium/project-configuration/' +
    'raw/branch/master'
)
NUM_TASKS = 3

FILE1_TXT = 'file1.txt'
FILE2_TXT = 'file2.txt'
FILE3_TXT = 'file3.txt'
FILE4_TXT = 'file4.txt'
FILE_CONTENT = b'file content'
ANOTHER_CONTENT = b'another content'
PATH = 'path'
TYPE = 'type'
BLOB_TYPE = 'blob'
TREE_TYPE = 'tree'

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'response_payload, expected_file_list',
    [
        (
            {
                'tree': [
                    {PATH: FILE1_TXT, TYPE: BLOB_TYPE},
                    {PATH: FILE2_TXT, TYPE: BLOB_TYPE},
                    {PATH: 'dir1', TYPE: TREE_TYPE},
                ],
            },
            [FILE1_TXT, FILE2_TXT],
        ),
        (
            {
                'tree': [
                    {'path': FILE3_TXT, 'type': BLOB_TYPE},
                    {'path': FILE4_TXT, 'type': BLOB_TYPE},
                ],
            },
            [FILE3_TXT, FILE4_TXT],
        ),
    ],
)
async def test_fetch_file_list(response_payload, expected_file_list):
    """Test fetching file list from the repository."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as ares:
            ares.get(REPO_URL, payload=response_payload)
            file_list = await fetch_file_list(session)

            assert file_list == expected_file_list


@pytest.mark.parametrize(
    'files, file_content',
    [
        ([FILE1_TXT, FILE2_TXT], FILE_CONTENT),
        ([FILE3_TXT, FILE4_TXT], ANOTHER_CONTENT),
    ],
)
async def test_download_files(tmp_path, files, file_content):
    """Test downloading files from the repository."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mock_response:
            for each_file in files:
                mock_response.get(
                    '{base_url}/{path}'.format(
                        base_url=BASE_RAW_URL,
                        path=each_file,
                    ),
                    body=file_content,
                )

            await download_files(session, files, BASE_RAW_URL, tmp_path)

            for d_file in files:
                file_path = tmp_path / d_file
                assert file_path.exists()
                assert file_path.read_bytes() == file_content


@pytest.mark.parametrize(
    'file_contents, expected_hashes',
    [
        (
            [(FILE1_TXT, FILE_CONTENT), (FILE2_TXT, FILE_CONTENT)],
            {
                FILE1_TXT: hashlib.sha256(FILE_CONTENT).hexdigest(),
                FILE2_TXT: hashlib.sha256(FILE_CONTENT).hexdigest(),
            },
        ),
        (
            [(FILE3_TXT, ANOTHER_CONTENT), (FILE4_TXT, ANOTHER_CONTENT)],
            {
                FILE3_TXT: hashlib.sha256(ANOTHER_CONTENT).hexdigest(),
                FILE4_TXT: hashlib.sha256(ANOTHER_CONTENT).hexdigest(),
            },
        ),
    ],
)
async def test_process_files(                               # noqa: WPS210
    tmp_path, file_contents, expected_hashes,
):
    """Test processing files to calculate their hashes."""
    file_paths = []
    for filename, file_content in file_contents:
        file_path = tmp_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(file_content)
        file_paths.append(file_path)

    with patch(
        'app.main.calculate_sha256',
        side_effect=lambda each: hashlib.sha256(each.read_bytes()).hexdigest(),
    ) as mock_calc:
        await process_files(file_paths)
        assert mock_calc.call_count == len(file_paths)
        for exp_file_path, expected_hash in expected_hashes.items():
            assert calculate_sha256(tmp_path / exp_file_path) == expected_hash


@pytest.mark.parametrize(
    'file_list, num_tasks, expected_chunks',
    [
        (
            [FILE1_TXT, FILE2_TXT, FILE3_TXT],
            2,
            [[FILE1_TXT, FILE2_TXT], [FILE3_TXT]],
        ),
        (
            [FILE1_TXT, FILE2_TXT, FILE3_TXT, FILE4_TXT],
            3,
            [[FILE1_TXT, FILE2_TXT], [FILE3_TXT], [FILE4_TXT]],
        ),
    ],
)
async def test_main(                                    # noqa: WPS210
    tmp_path, file_list, num_tasks, expected_chunks,
):
    """Test the main workflow of the application."""
    chunks = split_list(file_list, NUM_TASKS)

    with ((patch('app.main.fetch_file_list', return_value=file_list))):
        with patch('app.main.download_files') as mock_download_files:
            with patch('app.main.process_files') as mock_process_files:
                with patch(
                    'aiohttp.ClientSession.get',
                    new_callable=AsyncMock,
                ):
                    await main()

                # Verify the number of calls
                assert mock_download_files.call_count == NUM_TASKS

                # Extract call arguments for download_files
                call_args_list = [
                    call[0][1] for call in mock_download_files.call_args_list
                ]

                # Verify that each chunk was passed as an argument
                for chunk in chunks:
                    chunk_set = set(chunk)
                    assert any(
                        chunk_set == set(args) for args in call_args_list
                    ), 'Expected chunk {chunk_set} not found'.format(
                        chunk_set=chunk_set,
                    )

                # Ensure process_files is called once with all file paths
                assert mock_process_files.call_count == 1


@pytest.mark.parametrize(
    'file_content, expected_hash',
    [
        (FILE_CONTENT, hashlib.sha256(FILE_CONTENT).hexdigest()),
        (ANOTHER_CONTENT, hashlib.sha256(ANOTHER_CONTENT).hexdigest()),
    ],
)
def test_calculate_sha256(tmp_path, file_content, expected_hash):
    """Test calculating SHA-256 hash of a file."""
    file_path = tmp_path / 'file.txt'
    file_path.write_bytes(file_content)

    assert calculate_sha256(file_path) == expected_hash


@pytest.mark.parametrize(
    'file_list, num_tasks, expected_chunks',
    [
        (
            [FILE1_TXT, FILE2_TXT, FILE3_TXT],
            2,
            [[FILE1_TXT, FILE2_TXT], [FILE3_TXT]],
        ),
        (
            [FILE1_TXT, FILE2_TXT, FILE3_TXT, FILE4_TXT],
            3,
            [[FILE1_TXT, FILE2_TXT], [FILE3_TXT], [FILE4_TXT]],
        ),
    ],
)
def test_split_list(file_list, num_tasks, expected_chunks):
    """Test splitting a list into chunks."""
    chunks = split_list(file_list, num_tasks)

    assert len(chunks) == len(expected_chunks)
    for chunk, expected_chunk in zip(chunks, expected_chunks):
        assert set(chunk) == set(expected_chunk)
