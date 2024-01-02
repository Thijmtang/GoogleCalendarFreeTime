import string


class ScreenUtils:
    @staticmethod
    def getGeometry(width: int, height: int, screenWidth: int, screenHeight: int) -> string:
        'Used to center Tkinter widgets'
        # Calculate Starting X and Y coordinates for Window
        x = (screenWidth / 2) - (width / 2)
        y = (screenHeight / 2) - (height / 2)

        return '%dx%d+%d+%d' % (width, height, x, y)



