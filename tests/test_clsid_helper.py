import os

from app.utils.clsid_helper import get_path_from_folder_clsid


def test_get_path_from_clsid():
    """
    Test the get_path_from_clsid function with a known CLSID.
    """
    # Example CLSID for Program files
    clsid = "{6D809377-6AF0-444b-8957-A3773F02200E}"

    # Expected path for Program files
    expected_path = os.path.expandvars("%ProgramFiles%")

    # Call the function
    result = get_path_from_folder_clsid(clsid)

    # Assert that the result matches the expected path
    assert result == expected_path, f"Expected {expected_path}, but got {result}"