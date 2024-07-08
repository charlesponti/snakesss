import os


class FileRepository:
    @staticmethod
    def get_file_contents(filepath: str):
        dir = os.path.dirname(__file__)
        try:
            with open(f'{filepath}', 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
         raise FileNotFoundError(f"Error: {filepath} does not exist in the {dir} folder.")
        except Exception as e:
            return f"An error occurred: {str(e)}"