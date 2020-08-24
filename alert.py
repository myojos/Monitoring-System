import models


class Alert:
    def __init__(self, rule):
        self.checkers = {}
        try:
            for model_name in rule:
                model_rule = rule[model_name]
                model_class_ = getattr(models, model_name)
                self.checkers[model_name] = model_class_(model_rule)
        except KeyError as e:
            print('Configuration file struct is wrong. Error {e}'.format(e=e))

    def check(self, img_path, frame):
        found = True
        for checker_name in self.checkers:
            checker = self.checkers[checker_name]
            if not checker.check(img_path, frame):
                found = False
                break
        return found
