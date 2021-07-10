# will be a main menu(just a test class for now)

class mainMenu:
    def run(self, events, width, height):
        """Just returns a white screen with some Black on the bottom"""
        return "[rgb(255, 255, 255)]█[/rgb(255, 255, 255)]"*width*(height-10)+"[rgb(000, 000, 000)]█[/rgb(000, 000, " \
                                                                              "000)]"*10, 0
