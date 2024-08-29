import re
from typing import Any, Dict, List, Literal
from swarmauri.standard.tools.base.ToolBase import ToolBase
from swarmauri.standard.tools.concrete.Parameter import Parameter

class FleschKincaidTool(ToolBase):
    """
    A tool for calculating the Flesch-Kincaid readability scores.

    Attributes:
        version (str): The version of the tool.
        name (str): The name of the tool.
        type (Literal["FleschKincaidTool"]): The type of the tool.
        description (str): A brief description of what the tool does.
        parameters (List[Parameter]): The parameters for configuring the tool.
    """
    version: str = "0.1.dev1"
    name: str = "FleschKincaidTool"
    type: Literal["FleschKincaidTool"] = "FleschKincaidTool"
    description: str = "Calculates the Flesch-Kincaid readability scores for a given text."
    parameters: List[Parameter] = [
        Parameter(
            name="input_text",
            type="string",
            description="The input text for which to calculate the Flesch-Kincaid scores.",
            required=True
        )
    ]

    def __call__(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Executes the Flesch-Kincaid tool and returns both the Reading Ease and Grade Level scores.

        Flesch Reading Ease formula:
        Reading Ease = 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        
        Flesch-Kincaid Grade Level formula:
        Grade Level = 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        
        Parameters:
            data (Dict[str, Any]): The input data containing "input_text".
        
        Returns:
            Dict[str, float]: A dictionary with 'reading_ease' and 'grade_level' scores.

        Raises:
            ValueError: If the input data is invalid.
        """
        if self.validate_input(data):
            text = data['input_text']
            num_sentences = self.count_sentences(text)
            num_words = self.count_words(text)
            num_syllables = self.count_syllables(text)
            if num_sentences == 0 or num_words == 0:
                return {'reading_ease': 0.0, 'grade_level': 0.0}
            words_per_sentence = num_words / num_sentences
            syllables_per_word = num_syllables / num_words

            # Flesch Reading Ease score
            reading_ease = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
            
            # Flesch-Kincaid Grade Level
            grade_level = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
            
            return {'reading_ease': reading_ease, 'grade_level': grade_level}
        else:
            raise ValueError("Invalid input for FleschKincaidTool.")

    def count_sentences(self, text: str) -> int:
        """
        Counts the number of sentences in the text.
        
        Parameters:
            text (str): The input text.
        
        Returns:
            int: The number of sentences in the text.
        """
        sentence_endings = re.compile(r'[.!?]')
        sentences = sentence_endings.split(text)
        return len([s for s in sentences if s.strip()])  # Count non-empty sentences

    def count_words(self, text: str) -> int:
        """
        Counts the number of words in the text.
        
        Parameters:
            text (str): The input text.
        
        Returns:
            int: The number of words in the text.
        """
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def count_syllables(self, text: str) -> int:
        """
        Counts the number of syllables in the text.
        
        Parameters:
            text (str): The input text.
        
        Returns:
            int: The number of syllables in the text.
        """
        words = re.findall(r'\b\w+\b', text)
        syllable_count = 0
        for word in words:
            syllable_count += self.count_syllables_in_word(word)
        return syllable_count

    def count_syllables_in_word(self, word: str) -> int:
        """
        Counts the number of syllables in a single word.
        
        Parameters:
            word (str): The input word.
        
        Returns:
            int: The number of syllables in the word.
        """
        word = word.lower()
        vowels = "aeiouy"
        syllables = 0
        if len(word) == 0:
            return syllables
        if word[0] in vowels:
            syllables += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                syllables += 1
        if word.endswith('e'):
            syllables -= 1
        if syllables == 0:
            syllables = 1
        return syllables
