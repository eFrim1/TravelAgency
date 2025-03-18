import sys
from PyQt5.QtWidgets import QApplication
from view.view import View
from presenter.presenter import Presenter
from model.repository.repository import init_db

if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    view = View()
    view.show()
    
    sys.exit(app.exec_())
