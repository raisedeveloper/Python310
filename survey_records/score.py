class scoreCalculator:
    def __init__(self, question1, question2, question3, question4, question5):
        self.question1 = question1
        self.question2 = question2
        self.question3 = question3
        self.question4 = question4
        self.question5 = question5

    def get_score(self):
        """score 범주 반환"""
        score = self.question1+self.question2+self.question3+self.question4+self.question5
        
        if score < 6:
            return "환경파괴자"
        elif score < 11 :
            return "환경관심꾼"
        elif score < 16:
            return "환경지킴이"
        elif score < 21:
            return "환경사랑꾼"
        else:
            return "환경수호자"

    def get_result(self):
        """score 결과 반환"""
        score = self.get_score()
        
        return {
            "score": score,
            "question1": self.question1,
            "question2": self.question2,
            "question3": self.question3,
            "question4": self.question4,
            "question5": self.question5
        }