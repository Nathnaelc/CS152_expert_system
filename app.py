import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QLineEdit, QLabel, QTextEdit, QFormLayout)
import spacy
from pyswip import Prolog
# Load English NLP model
nlp = spacy.load('en_core_web_sm')


class ExpertSystemGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Expert System Interface')

        # Main layout
        self.layout = QVBoxLayout(self)

        # Introduction label
        self.introLabel = QLabel(
            "Welcome to Buenos Aires's Sports Facility Recommendation System")
        self.introLabel.setWordWrap(True)
        self.layout.addWidget(self.introLabel)

        # Form layout for inputs
        self.formLayout = QFormLayout()
        self.textInput = QLineEdit(self)
        self.formLayout.addRow(
            'Enter your preferences in natural language:', self.textInput)
        self.layout.addLayout(self.formLayout)

        # Button for getting recommendations
        self.button = QPushButton('Get Recommendation', self)
        self.button.clicked.connect(self.on_click)
        self.layout.addWidget(self.button)

        # Text area for displaying results
        self.resultsText = QTextEdit(self)
        self.resultsText.setReadOnly(True)
        self.layout.addWidget(self.resultsText)

        self.show()

    def on_click(self):
        user_input = self.textInput.text()
        doc = nlp(user_input)

        # Extracting information
        sport = None
        location = None
        for token in doc:
            # Check against a more comprehensive list of sports
            if token.text.lower() in ["soccer", "tennis", "rugby", "polo", "equestrian", "basketball", "running", "cycling", "hiking", "biking", "swimming", "golf"]:
                sport = token.text.lower()
            if token.ent_type_ == "GPE":
                location = token.text

        # Invoke Prolog query with extracted information
        if sport and location:
            self.query_prolog_and_display_results(sport, location)
        else:
            self.resultsText.setText(
                "Could not extract the necessary information.")

    def query_prolog_and_display_results(self, sport, location):
        prolog = Prolog()
        # consult the Prolog rules
        prolog.consult("recommendation_rules.pl")

        # Formulate the query string
        query_string = f"recommend_facility({sport}, {location}, _, _, Facility)"
        results = list(prolog.query(query_string))

        # Display the results
        if results:
            facilities = [result["Facility"] for result in results]
            self.resultsText.setText(
                "Recommended facilities:\n" + "\n".join(facilities))
        else:
            self.resultsText.setText("No matching facilities found.")


def main():
    app = QApplication(sys.argv)
    ex = ExpertSystemGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
