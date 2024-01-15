import pytest
from project import check_character_existence, initialize_conversation, get_completion_from_messages

# Define test data
valid_source_material = ["Harry Potter", "harry ptter", "Harry Potter and the Sorcerer's Stone"]
invalid_source_material = ["hdfhdfsk", "family guy", "LotR"]
valid_characters = ["Harry", "hermione", "Ron Weasley", "Hedwig"]
invalid_characters = ["Cory", "Topanga", "wizard", "Darth Vader"]
setting_list = ["in the Forbidden Forest", "In the Great Hall", "walking to Hogsmeade", "in the Chamber of Secrets"]

# # Test check_character_existence() and check_source_completion()
# # Check valid_source and valid_character
# @pytest.mark.parametrize("source_material, character", [(s, c) for s in valid_source_material for c in valid_characters])
# def test_check_character_existence(source_material, character):
#     source_check = check_character_existence(source_material, character)
#     assert source_check.lower() == 'diverse' or source_check.lower() == 'female' or source_check.lower() == 'male'

# # Check invalid_source and invalid_character
# @pytest.mark.parametrize("source_material, character", [(s, c) for s in invalid_source_material for c in invalid_characters])
# def test_check_character_existence_invalid_1(source_material, character):
#     source_check = check_character_existence(source_material, character)
#     assert source_check.lower() == 'no'

# # Check valid_source and invalid_character
# @pytest.mark.parametrize("source_material, character", [(s, c) for s in valid_source_material for c in invalid_characters])
# def test_check_character_existence_invalid_2(source_material, character):
#     source_check = check_character_existence(source_material, character)
#     assert source_check.lower() == 'no'

# # Check invalid_source and valid_character
# @pytest.mark.parametrize("source_material, character", [(s, c) for s in invalid_source_material for c in valid_characters])
# def test_check_character_existence_invalid_3(source_material, character):
#     source_check = check_character_existence(source_material, character)
#     assert source_check.lower() == 'no'


# # Test initialize_conversation and get_completion_from_messages function -- GENERIC CHECK
# def test_initialize_conversation():
#     conversation = initialize_conversation(valid_source_material[0], valid_characters[0], setting_list[0])
#     assert len(conversation) == 1
#     assert isinstance(conversation[0], dict)
#     assert "system" in conversation[0]["role"]
#     assert valid_source_material[0] in conversation[0]["content"]
#     assert valid_characters[0] in conversation[0]["content"]
#     assert setting_list[0] in conversation[0]["content"]

# def test_get_completion_from_messages():
#     messages = [
#         {"role": "user", "content": "Tell me a joke."},
#         {"role": "assistant", "content": "Why did the chicken cross the road?"},
#     ]
#     response = get_completion_from_messages(messages)
#     assert isinstance(response, str)
#     assert response != ""

# Test initialize_conversation and get_completion_from_messages function -- SPECIFIC TEST 
def test_initialize_conversation_specific():
    conversation = initialize_conversation(valid_source_material[0], valid_characters[1], setting_list[0])
    assert len(conversation) == 1
    assert isinstance(conversation[0], dict)
    assert "system" in conversation[0]["role"]
    assert valid_source_material[0] in conversation[0]["content"]
    assert valid_characters[0] in conversation[0]["content"]
    assert setting_list[0] in conversation[0]["content"]

# Provide source = "Harry Potter", character = "Hermione", setting = "in the Forbidden Forest"
def test_get_completion_from_messages_specific():
    conversation = initialize_conversation(valid_source_material[0], valid_characters[1], setting_list[0])
    conversation.append(
        {
            "role": "user", "content": '''Hi! What's your name? And do you happen to know the name of this forest?'''
        },
    )
    response = get_completion_from_messages(conversation)
    assert isinstance(response, str)
    responses = response.split(" ")
    assert "Hermione" in responses
    assert "Forbidden" in responses