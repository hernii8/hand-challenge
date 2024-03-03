from typing import Any, Dict, List
from enum import Enum


class Emojis(Enum):
    POINT_RIGHT = "👉"
    POINT_LEFT = "👈"
    POINT_DOWN = "👇"
    POINT_UP = "👆"
    FIST = "👊"
    FIST_RIGHT = "🤜"
    FIST_LEFT = "🤛"


class Decoder:
    def __init__(self, code: str) -> None:
        self.code_cursor = 0
        self.memory_cursor = 0
        self.memory: List[int] = [0]
        self.return_sequence = ""
        self.code = code

    def actions(self) -> Dict[str, Any]:
        return {
            Emojis.POINT_RIGHT.value: self.__move_right,
            Emojis.POINT_LEFT.value: self.__move_left,
            Emojis.POINT_UP.value: self.__increment_memory,
            Emojis.POINT_DOWN.value: self.__decrease_memory,
            Emojis.FIST.value: self.__print,
            Emojis.FIST_RIGHT.value: self.__jump_to_next,
            Emojis.FIST_LEFT.value: self.__jump_to_previous,
        }

    def decodify(self) -> str:
        while self.code_cursor < len(self.code):
            key = self.code[self.code_cursor]
            self.code_cursor += 1
            self.actions()[key]()

        return self.return_sequence

    def __move_right(self) -> None:
        if self.memory_cursor + 1 > len(self.memory) - 1:
            self.memory.append(0)
        self.memory_cursor += 1

    def __move_left(self) -> None:
        if self.memory_cursor > 0:
            self.memory_cursor -= 1

    def __increment_memory(self) -> None:
        self.memory[self.memory_cursor] += 1
        if self.memory[self.memory_cursor] > 255:
            self.memory[self.memory_cursor] = 0

    def __decrease_memory(self) -> None:
        self.memory[self.memory_cursor] -= 1
        if self.memory[self.memory_cursor] < 0:
            self.memory[self.memory_cursor] = 255

    def __jump_to_next(self) -> None:
        if self.memory[self.memory_cursor] == 0:
            remaining_characters = list(self.code[self.code_cursor :])
            nesting_depth = 1
            characters_to_advance = 0
            while nesting_depth > 0:
                next_character = remaining_characters.pop(0)
                if next_character == Emojis.FIST_LEFT.value:
                    nesting_depth -= 1
                elif next_character == Emojis.FIST_RIGHT.value:
                    nesting_depth += 1
                if nesting_depth == 0:
                    self.code_cursor += characters_to_advance + 1
                    break
                characters_to_advance += 1

    def __jump_to_previous(self) -> None:
        if self.memory[self.memory_cursor] != 0:
            remaining_characters = list(self.code[: self.code_cursor - 1])
            nesting_depth = 1
            characters_to_advance = 0
            while nesting_depth > 0:
                next_character = remaining_characters.pop()
                if next_character == Emojis.FIST_RIGHT.value:
                    nesting_depth -= 1
                elif next_character == Emojis.FIST_LEFT.value:
                    nesting_depth += 1
                if nesting_depth == 0:
                    self.code_cursor -= characters_to_advance + 1
                    break
                characters_to_advance += 1

    def __print(self):
        self.return_sequence += chr(self.memory[self.memory_cursor])


def test_hello():
    """It should decodify the sequence given to a 'Hello'"""
    start_sequence = "👇🤜👇👇👇👇👇👇👇👉👆👈🤛👉👇👊👇🤜👇👉👆👆👆👆👆👈🤛👉👆👆👊👆👆👆👆👆👆👆👊👊👆👆👆👊"
    decoded = Decoder(code=start_sequence).decodify()
    assert decoded == "Hello"


def test_hello_world():
    """It should decodify the sequence given to a 'Hello World!'"""
    start_sequence = "👉👆👆👆👆👆👆👆👆🤜👇👈👆👆👆👆👆👆👆👆👆👉🤛👈👊👉👉👆👉👇🤜👆🤛👆👆👉👆👆👉👆👆👆🤜👉🤜👇👉👆👆👆👈👈👆👆👆👉🤛👈👈🤛👉👇👇👇👇👇👊👉👇👉👆👆👆👊👊👆👆👆👊👉👇👊👈👈👆🤜👉🤜👆👉👆🤛👉👉🤛👈👇👇👇👇👇👇👇👇👇👇👇👇👇👇👊👉👉👊👆👆👆👊👇👇👇👇👇👇👊👇👇👇👇👇👇👇👇👊👉👆👊👉👆👊"
    decoded = Decoder(code=start_sequence).decodify()
    assert decoded == "Hello World!\n"
