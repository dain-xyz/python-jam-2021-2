# will be a main menu(just a test class for now)

class mainMenu:
    """Will be a main menu, its a test place for now"""

    def run(self, events:list[str], width:int, height:int)->tuple[str, int]:
        """Just returns a white screen with some Black on the bottom"""

        return "[rgb(255, 255, 255)]█[/rgb(255, 255, 255)]"*width*(height-10)+"[rgb(000, 000, 000)]█[/rgb(000, 000, " \
                                                                              "000)]"*10, 0
