import pytest
from project import (
    check_source_material,
    initialize_conversation,
    get_completion_from_messages,
)

# Define some test data
valid_source_material = "Harry Potter"
invalid_source_material = "Invalid Source Material"
valid_character = "Harry Potter"
setting = "Hogwarts School of Witchcraft and Wizardry"


# Test check_source_material function
def test_check_valid_source_material():
    assert check_source_material(valid_source_material) is True


def test_check_invalid_source_material():
    assert check_source_material(invalid_source_material) is False


# Test initialize_conversation function
def test_initialize_conversation():
    conversation = initialize_conversation(valid_source_material, valid_character, setting)
    assert len(conversation) == 1
    assert isinstance(conversation[0], dict)
    assert "system" in conversation[0]["role"]
    assert valid_source_material in conversation[0]["content"]
    assert valid_character in conversation[0]["content"]
    assert setting in conversation[0]["content"]


# Test get_completion_from_messages functions
def test_get_completion_from_messages():
    messages = [
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": "Why did the chicken cross the road?"},
    ]
    response = get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.7)
    assert isinstance(response, str)
    assert response != ""


if __name__ == "__main__":
    pytest.main()
