import pytest
from app.common import merge_into


@pytest.mark.parametrize('initial, updates, expected', [(
        {'name': 'Margot', 'integer': 1337},
        {'integer': 777, 'robot': 'pupper'},
        {'name': 'Margot', 'integer': 777, 'robot': 'pupper'}
),
    (
            {'name': 'Margot', 'integer': 1337, 'another_dict': {
                "key1": "value1", "key2": "value2"
            }},
            {'integer': 777, 'robot': 'pupper', 'another_dict': {
                "key2": "mod_value2", "key3": "value3"
            }},
            {'name': 'Margot', 'integer': 777, 'robot': 'pupper', 'another_dict': {
                "key1": "value1", "key2": "mod_value2", "key3": "value3"
            }}
    )
])
def test_merge_into(initial, updates, expected):
    result = merge_into(initial, updates)
    assert result == expected
