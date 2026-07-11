"""Tests for read_file resource limits."""

from nanobot.agent.tools.filesystem import ReadFileTool


async def test_read_file_rejects_oversized_files(tmp_path):
    path = tmp_path / "large.txt"
    with path.open("wb") as handle:
        handle.truncate(ReadFileTool._MAX_READ_BYTES + 1)

    tool = ReadFileTool(workspace=tmp_path, allowed_dir=tmp_path)
    result = await tool.execute(path="large.txt")

    assert "too large to read safely" in result
