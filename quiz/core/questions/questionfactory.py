from core.questions.question import Question

class QuestionFactory:

    @staticmethod
    def create_question(jobj, key):
        text = jobj[key]["text"]
        diff = jobj[key]["difficulty"]
        correct_ans = jobj[key]["correct"]
        answers = jobj[key]["answers"]

        return Question(text, diff, answers, correct_ans)