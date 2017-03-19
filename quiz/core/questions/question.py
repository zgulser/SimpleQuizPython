class Question:

    NUMBER_OF_ANSWERS = 4

    def __init__(self, question, difficulty, answers, correct_ans):
        self.question = question
        self.difficulty = difficulty
        self.correct_ans = correct_ans
        self.answer_map = {}

        self.setup_answers(answers)

    def setup_answers(self, answers):
        for item in answers:
            self.answer_map[item["option"]] = item["answer"]
            continue

    def is_correct_answer(self, answer_given):
        return answer_given == self.correct_ans
