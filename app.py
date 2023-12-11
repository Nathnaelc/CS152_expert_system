import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QTextEdit, QFormLayout, QComboBox, QCheckBox
from PyQt5.QtCore import QThread, pyqtSignal
import spacy
from pyswip.prolog import Prolog
import logging
import os

logging.basicConfig(level=logging.INFO)
nlp = spacy.load('en_core_web_sm')


class PrologQueryThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, sport, location, budget, skill_level, indoor_outdoor):
        QThread.__init__(self)
        self.sport = sport
        self.location = location
        self.budget = budget
        self.skill_level = skill_level
        self.indoor_outdoor = indoor_outdoor

    def run(self):
        try:
            prolog = Prolog()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            prolog_file = os.path.join(dir_path, "recommendation_rules.pl")
            prolog.consult(prolog_file)

            query_string = f"recommend_facility('{self.sport}', '{self.location}', '{self.budget}', '{self.skill_level}', '{self.indoor_outdoor}', Facility)"
            results = list(prolog.query(query_string))

            if results:
                facilities = [result["Facility"] for result in results]
                display_text = "Recommended facilities:\n" + \
                    "\n".join(facilities)
            else:
                display_text = "No matching facilities found."
        except Exception as e:
            display_text = f"Error in querying Prolog: {e}"

        self.result_signal.emit(display_text)


class ExpertSystemGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.query_thread = None
        self.sport = None
        self.location = None
        self.additionalQuestionsRendered = False  # Flag to track state

    def initUI(self):
        self.setWindowTitle("Expert System Interface")
        self.layout = QVBoxLayout(self)
        self.introLabel = QLabel(
            "Welcome to Buenos Aires's Sports Facility Recommendation System")
        self.introLabel.setWordWrap(True)
        self.layout.addWidget(self.introLabel)
        self.locationInput = QLineEdit(self)

        # open-ended initial question
        self.questionLabel = QLabel(
            "What activity are you interested in or where would you like to play?", self)
        self.layout.addWidget(self.questionLabel)

        self.formLayout = QFormLayout()
        self.textInput = QLineEdit(self)
        self.formLayout.addRow(self.questionLabel, self.textInput)
        self.layout.addLayout(self.formLayout)

        self.processInputButton = QPushButton('Process Input', self)
        self.processInputButton.clicked.connect(self.on_process_input_click)
        self.layout.addWidget(self.processInputButton)

        # Initialize additional widgets but don't add them yet
        self.initialize_additional_widgets()

        self.resultsText = QTextEdit(self)
        self.resultsText.setReadOnly(True)
        self.layout.addWidget(self.resultsText)
        self.show()

    def initialize_additional_widgets(self):
        self.budgetDropdown = QComboBox(self)
        self.budgetDropdown.addItems(["free", "moderate", "expensive"])
        self.skillLevelDropdown = QComboBox(self)
        self.skillLevelDropdown.addItems(
            ["beginner", "intermediate", "advanced", "all_levels"])
        self.indoorOutdoorCheckbox = QCheckBox("Indoor", self)
        self.getRecommendationButton = QPushButton('Get Recommendation', self)
        self.getRecommendationButton.clicked.connect(
            self.on_get_recommendation_click)

    def update_ui_with_additional_questions(self):
        if not self.additionalQuestionsRendered:
            self.formLayout.addRow('Budget:', self.budgetDropdown)
            self.formLayout.addRow('Skill Level:', self.skillLevelDropdown)
            self.formLayout.addRow(
                'Indoor/Outdoor Preference:', self.indoorOutdoorCheckbox)
            self.layout.addWidget(self.getRecommendationButton)
            self.additionalQuestionsRendered = True

    def query_prolog_and_display_results(self, sport, location, budget, skill_level, indoor_outdoor):
        try:
            prolog = Prolog()
            prolog.consult("recommendation_rules.pl")

            query_string = f"recommend_facility('{sport}', '{location}', '{budget}', '{skill_level}', '{indoor_outdoor}', Facility)"
            print(f"Querying Prolog with: {query_string}")  # Debugging
            results = list(prolog.query(query_string))
            print(f"Results: {results}")  # Debugging

            if results:
                facilities = [result["Facility"] for result in results]
                self.resultsText.setText(
                    "Recommended facilities:\n" + "\n".join(facilities))
            else:
                self.resultsText.setText("No matching facilities found.")
        except Exception as e:
            self.resultsText.setText(f"Error in querying Prolog: {e}")
            print(f"Prolog query error: {e}")  # Debugging

    def on_process_input_click(self):
        user_input = self.textInput.text()
        print(f"User input: {user_input}")  # Debugging
        doc = nlp(user_input)
        self.sport, self.location = self.extract_info(doc)

        if self.sport and self.location:
            print("Both sport and location extracted, querying Prolog...")
            self.query_prolog_and_display_results(
                self.sport, self.location, 'free', 'beginner', 'outdoor')
        elif self.sport or self.location:
            print(
                f"Partial info extracted - Sport: {self.sport}, Location: {self.location}")
            self.ask_follow_up_questions()
        else:
            self.resultsText.setText(
                "Could not extract the necessary information.")
            print("Failed to extract necessary information.")  # Debugging

    def on_get_recommendation_click(self):
        budget = self.budgetDropdown.currentText()
        skill_level = self.skillLevelDropdown.currentText()
        indoor_outdoor = 'indoor' if self.indoorOutdoorCheckbox.isChecked() else 'outdoor'
        location = self.location if self.location else self.locationInput.text()
        self.query_prolog_and_display_results(
            self.sport, location, budget, skill_level, indoor_outdoor)

    def on_process_input_click(self):
        user_input = self.textInput.text()
        print(f"User input: {user_input}")  # Debugging
        doc = nlp(user_input)
        self.sport, self.location = self.extract_info(doc)

        if self.sport or self.location:
            print(
                f"Partial info extracted - Sport: {self.sport}, Location: {self.location}")
            self.ask_follow_up_questions()
        else:
            self.resultsText.setText(
                "Could not extract the necessary information.")
            print("Failed to extract necessary information.")  # Debugging

    def ask_follow_up_questions(self):
        self.textInput.clear()

        if not self.sport:
            self.layout.addWidget(QLabel("What sport are you interested in?"))
            self.layout.addWidget(self.skillLevelDropdown)

        if not self.location:
            self.layout.addWidget(QLabel("Where would you like to play?"))
            self.layout.addWidget(self.locationInput)

        # to ensure additional questions and widgets are added only once
        if not self.additionalQuestionsRendered:
            self.layout.addWidget(self.getRecommendationButton)
            self.layout.addWidget(self.indoorOutdoorCheckbox)
            self.additionalQuestionsRendered = True

    def prompt_for_location(self):
        self.locationLabel = QLabel(
            "Please enter your preferred location:", self)
        self.locationInput = QLineEdit(self)
        self.formLayout.addRow(self.locationLabel, self.locationInput)

    def extract_info(self, doc):
        sport = None
        location = None
        sports_keywords = ["soccer", "tennis", "rugby", "polo", "equestrian",
                           "basketball", "running", "cycling", "hiking", "biking", "swimming", "golf"]
        neighborhoods = ["palermo", "recoleta", "belgrano", "nunez", "caballito", "la_boca", "san_telmo", "puerto_madero", "retiro", "san_nicolas", "monserrat", "san_cristobal", "barracas", "constitucion", "flores", "floresta", "paternal", "villa_crespo", "almagro", "boedo",
                         "parque_patricios", "liniers", "mataderos", "versalles", "villa_luro", "villa_devoto", "villa_del_parque", "villa_general_mitre", "villa_ortuzar", "villa_pueyrredon", "villa_real", "villa_riachuelo", "villa_santa_rita", "villa_soldati", "villa_urquiza", "villa_lugano"]

        for token in doc:
            if token.text.lower() in sports_keywords:
                sport = token.text.lower()
            elif token.text.lower() in neighborhoods:
                location = token.text.lower()

        # For debugging
        print(f"Extracted info - Sport: {sport}, Location: {location}")
        return sport, location


def main():
    app = QApplication(sys.argv)
    ex = ExpertSystemGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
