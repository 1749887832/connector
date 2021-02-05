class ChangeKeyword:
    def __init__(self):
        super().__init__()

    def ChangeData(self, change_data):
        if 'true' in change_data:
            data = change_data.replace('true', 'True')
        elif 'false' in change_data:
            data = change_data.replace('false', 'False')
        else:
            data = change_data
        return data
