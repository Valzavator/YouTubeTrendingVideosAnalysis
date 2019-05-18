import os


class Form:

    def launch(self):
        pass

    @staticmethod
    def get_user_input(string: str, to_clear=False):
        while True:
            if to_clear:
                os.system('cls')
            input_string = input(string).strip()
            if len(input_string) > 0:
                return input_string
