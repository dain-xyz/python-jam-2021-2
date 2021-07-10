# a class which loads other "utilities" and runs them
from rich.console import Console


class loader:
    # class of current  utility being used
    currentUtility = None
    console = Console()

    def load(self, filename: str) -> int:
        """Loads a class utility and loads that into the run function. Return a error code (0 is ok, 1 is an error
        occurred """
        try:
            exec(f"from microUtilities.{filename} import {filename}")
            exec(f"self.currentUtility = {filename}()")
            return 0
        except ImportError:
            return 1

    def tick(self) -> int:
        """Runs the classses main function once and displays it. If the class returns 0, its fine, else the class
        will return a 1 for exit and 2 for error. This function will pass on that info """

        # will be a list of events e.g. keypresses etc
        events = []

        out, code = self.currentUtility.run(events, self.console.width, self.console.height)
        self.console.print(out)

        return code

    def run(self):
        """Just ticks forever and if there is a crash or exit, goes to main menu"""
        while True:
            code = self.tick()
            if code != 0:
                self.load("mainMenu.py")
