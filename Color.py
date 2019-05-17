class Color_Manager:
    class BG:
        Black = '\033[40m'
        Red = '\033[41m'
        Green = '\033[42m'
        Yellow = '\033[43m'
        Blue = '\033[44m'
        Magenta = '\033[45m'
        Cyan = '\033[46m'
        White = '\033[47m'
        Reset = '\033[49m'
    class FG:
        Black = '\033[30m'
        Red = '\033[31m'
        Green = '\033[32m'
        Yellow = '\033[33m'
        Blue = '\033[34m'
        Magenta = '\033[35m'
        Cyan = '\033[36m'
        White = '\033[37m'
        Reset = '\033[39m'
    class BRIGHT:
        dim = '\033[2m'
        normal = '\033[22m'
    class EFFECT:
        ResetAll = '\033[0m'
        Italic = '\033[3m'
        Underline = '\033[4m'
        Bold = '\033[1m'
    @classmethod
    def FgPrint(cls, str, color):
        if color == 'Black':
            print(cls.FG.Black + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Red':
            print(cls.FG.Red + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Green':
            print(cls.FG.Green + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Yellow':
            print(cls.FG.Yellow + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Blue':
            print(cls.FG.Blue + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Magenta':
            print(cls.FG.Magenta + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Cyan':
            print(cls.FG.Cyan + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'White':
            print(cls.FG.White + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
    @classmethod
    def BgPrint(cls, str, color):
        if color == 'Black':
            print(cls.BG.Black + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Red':
            print(cls.BG.Red + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Green':
            print(cls.BG.Green + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Yellow':
            print(cls.BG.Yellow + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Blue':
            print(cls.BG.Blue + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Magenta':
            print(cls.BG.Magenta + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'Cyan':
            print(cls.BG.Cyan + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
        elif color == 'White':
            print(cls.BG.White + cls.EFFECT.Bold + str + cls.EFFECT.ResetAll, end = ' ')
