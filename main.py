from utils.panel import Panel
from utils.config import get_current_user


if __name__ == "__main__":
    panel = Panel()
    while True:
        if not get_current_user():
            panel.signing_panel()
        system = panel.system_panel()
        if not system:
            break
