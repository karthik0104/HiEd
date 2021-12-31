"""
File for storing all major constants required by the application.
"""

# Required fields constants
REQUIRED_FIELDS_FOR_WORD_TAG = ['user_id', 'dataset_id', 'word_id']

# Prefix constants
WORD_TAG_KEY_PREFIX = "word_tag:{dataset_id}:{user_id}"
TOKEN_FIRST_LETTER_PREFIX = "token:{dataset_id}:{token_first_letter}"
WORD_FIRST_LETTER_PREFIX = "word:{dataset_id}:{word_first_letter}"