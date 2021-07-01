class TestInput:
    def test_count_of_input_characters_is_less_than_15(self):
        expected_characters_count = 15
        phrase = input("Set a phrase: ")
        assert len(phrase) < expected_characters_count, f"Actual characters count is: {len(phrase)}, expected to be less than: {expected_characters_count}"
