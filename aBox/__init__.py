# Entry point
from loader import loader

if __name__ == '__main__':
    main_loader = loader()
    main_loader.load("mainMenu")
    main_loader.tick()
