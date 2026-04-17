
from unittest import TestCase

from Fuzzymatching import Fuzzymatch




# Test 1: Check if a perfect match returns the correct email
def test_exact_match():
    # Use your actual Excel path
    path = "/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx"
    matcher = Fuzzymatch(path)
    
    # Replace 'IT Support' with a department name actually in your Excel
    result = matcher.find_department("IT Support")
    assert "IT_Support@huddersfield.com" in result




# Test 2: Check if fuzzy matching handles typos
def test_fuzzy_match_typo():
    path = "/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx"
    matcher = Fuzzymatch(path)
    
    
    result = matcher.find_department("Ppoint")
    assert result is not None
    assert "@huddersfield.com" in result





















