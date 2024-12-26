import pytest
from seq import calculate_statistics

def test_a_seq():
    seq = "ACCTGXXCXXGTTACTGGGCXTTGTXX"
    stats = calculate_statistics(seq)
    total = sum(stats.values())  # Calculate total manually
    assert stats == {"A": 2, "C": 5, "G": 6, "T": 7, "Un": 7}
    assert total == 27  # Ensure total matches expected value

def test_b_seq():
    seq = "ACCGGGTTTT"
    stats = calculate_statistics(seq)
    total = sum(stats.values())  # Calculate total manually
    assert stats == {"A": 1, "C": 2, "G": 3, "T": 4, "Un": 0}
    assert total == 10  # Ensure total matches expected value