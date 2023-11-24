import pytest
from morfo import check_overlap

def test_check_overlap_no_overlap():
    # Test case where there is no overlap between two rectangles
    assert not check_overlap(0, 0, 100, 100, 200, 200, 300, 300)

def test_check_overlap_overlap():
    # Test case where there is an overlap between two rectangles
    assert check_overlap(0, 0, 100, 100, 50, 50, 150, 150)

if __name__ == "__main__":
    pytest.main()