from pandas import DataFrame
from pybatfish.datamodel.answer import TableAnswer
from pybatfish.question.question import QuestionBase


class MockTableAnswer(TableAnswer):
    def __init__(self, frame_to_use=DataFrame()):
        self._frame = frame_to_use

    def frame(self):
        return self._frame


class MockQuestion(QuestionBase):
    def __init__(self, answer=None):
        self._answer = answer if answer is not None else MockTableAnswer()

    def answer(self, *args, **kwargs):
        return self._answer
