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
        self.budget = 'free'
        self.skill_level = 'beginner'
        self.indoor_outdoor = 'outdoor'
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
        self.indoorOutdoorCheckbox = QComboBox(self)
        self.indoorOutdoorCheckbox.addItems(
            ["indoor", "outdoor", "indoor_outdoor"])
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

    def query_prolog_and_display_results(self):
        # Building and executing the Prolog query
        try:
            prolog = Prolog()
            prolog.consult("recommendation_rules.pl")

            # Dynamically build the Prolog query string
            query_parts = [self.sport, self.location, self.budget,
                           self.skill_level, "_", self.indoor_outdoor]
            query_parts = [part if part !=
                           'any' else '_' for part in query_parts]
            query_string = "recommend_facility({}, {}, {}, {}, {}, Facility)".format(
                *query_parts)
            print(f"Querying Prolog with: {query_string}")  # Debugging

            results = list(prolog.query(query_string))
            if results:
                facilities = [result["Facility"] for result in results]
                self.resultsText.setText(
                    "Recommended facilities:\n" + "\n".join(facilities))
            else:
                self.resultsText.setText("No matching facilities found.")
        except Exception as e:
            self.resultsText.setText(f"Error in querying Prolog: {e}")

    def process_input(self, user_input):
        if 'no preference' in user_input:
            self.handle_general_input()
            return

        if not self.sport:
            self.handle_sport_input(user_input)
        elif not self.location:
            self.handle_location_input(user_input)
        else:
            self.handle_additional_inputs()

    def handle_general_input(self):
        # Handle the case where the user has no specific preference
        self.sport = 'various_sports'
        self.location = 'any'
        self.budget = 'any'
        self.skill_level = 'all_levels'
        self.indoor_outdoor = 'any'
        self.query_prolog_and_display_results()

    def ask_location_question(self):
        self.layout.addWidget(QLabel("Where would you like to play?"))
        self.locationInput.clear()
        self.layout.addWidget(self.locationInput)

    def handle_sport_input(self, user_input):
        # Handle the case where the user has a sport preference
        self.sport = user_input if user_input != 'any' else 'various_sports'
        self.ask_location_question()

    def handle_location_input(self, user_input):
        # Handle specific location input and proceed to additional questions
        self.location = user_input if user_input != 'any' else 'any'
        self.ask_budget_question()

    def handle_additional_inputs(self):
        # Handle additional inputs based on current state
        if not self.budget:
            self.budget = self.budgetDropdown.currentText()
        if not self.skill_level:
            self.skill_level = self.skillLevelDropdown.currentText()
        if not self.indoor_outdoor:
            self.indoor_outdoor = self.indoorOutdoorCheckbox.currentText()
        self.query_prolog_and_display_results()

    def on_process_input_click(self):
        user_input = self.textInput.text().lower().strip()
        self.textInput.clear()  # Clear the input field for the next interaction
        doc = nlp(user_input)
        self.sport, self.location = self.extract_info(doc)

        if 'no preference' in user_input:
            self.display_general_choices()
        elif self.sport and self.location:
            # Both sport and location are known, proceed to additional questions
            self.ask_additional_questions()
        elif not self.sport:
            # Sport is unknown, ask about it
            self.ask_sport_question()
        elif not self.location:
            # Location is unknown, ask about it
            self.ask_location_question()
        else:
            # Something unexpected happened
            self.resultsText.setText("Please provide more information.")

    def display_general_choices(self):
        # Display popular or general choices and the 'Get Recommendation' button
        self.resultsText.setText("Suggesting popular/general choices...")
        self.layout.addWidget(self.getRecommendationButton)

    def ask_sport_question(self):
        self.layout.addWidget(QLabel("What sport are you interested in?"))
        # Temporary use for sport selection
        self.layout.addWidget(self.skillLevelDropdown)

    def ask_budget_question(self):
        self.layout.addWidget(QLabel("What is your budget preference?"))
        self.layout.addWidget(self.budgetDropdown)
        self.ask_skill_level_question()

    def ask_skill_level_question(self):
        self.layout.addWidget(QLabel("What is your skill level?"))
        self.layout.addWidget(self.skillLevelDropdown)
        self.ask_preferences_question()

    def ask_preferences_question(self):
        self.layout.addWidget(QLabel("Any indoor/outdoor preference?"))
        self.layout.addWidget(self.indoorOutdoorCheckbox)
        self.layout.addWidget(self.getRecommendationButton)

    def ask_missing_questions(self):
        if not self.sport:
            self.layout.addWidget(QLabel("What sport are you interested in?"))
            self.layout.addWidget(self.skillLevelDropdown)

        if not self.location:
            self.layout.addWidget(QLabel("Where would you like to play?"))
            self.locationInput.clear()
            self.layout.addWidget(self.locationInput)

        self.ask_budget_question()

    def ask_additional_questions(self):
        self.ask_budget_question()
        self.ask_skill_level_question()
        self.ask_preferences_question()

    def get_recommendation(self):
        # Only call query method if we have enough info
        if self.sport and self.location:
            self.query_prolog_and_display_results(
                self.sport, self.location, self.budget, self.skill_level, self.indoor_outdoor)
        else:
            self.resultsText.setText(
                "Please provide more information to get recommendations.")

    def on_get_recommendation_click(self):
        # Update askables based on current selection
        self.budget = self.budgetDropdown.currentText()
        self.skill_level = self.skillLevelDropdown.currentText()
        self.indoor_outdoor = self.indoorOutdoorCheckbox.currentText()
        self.location = self.location if self.location else self.locationInput.text()
        # Call the query method without parameters
        self.query_prolog_and_display_results()

    def ask_follow_up_questions(self):
        self.formLayout.removeRow(self.textInput)
        if not self.sport:
            self.layout.addWidget(QLabel("What sport are you interested in?"))
            self.layout.addWidget(self.skillLevelDropdown)

        if not self.location:
            self.layout.addWidget(QLabel("Where would you like to play?"))
            self.layout.addWidget(self.locationInput)

        if not self.additionalQuestionsRendered:
            self.update_ui_with_additional_questions()

    def prompt_for_location(self):
        self.locationLabel = QLabel(
            "Please enter your preferred location:", self)
        self.locationInput = QLineEdit(self)
        self.formLayout.addRow(self.locationLabel, self.locationInput)

    def update_ui_with_additional_questions(self):
        self.layout.addWidget(self.budgetDropdown)
        self.layout.addWidget(self.indoorOutdoorCheckbox)
        self.layout.addWidget(self.getRecommendationButton)
        self.additionalQuestionsRendered = True

    def build_prolog_query(self):
        # Dynamically build the Prolog query string
        query_parts = []
        query_parts.append(
            f"'{self.sport}'") if self.sport != 'any' else query_parts.append("_")
        query_parts.append(
            f"'{self.location}'") if self.location != 'any' else query_parts.append("_")
        query_parts.append(
            f"'{self.budget}'") if self.budget != 'any' else query_parts.append("_")
        query_parts.append(
            f"'{self.skill_level}'") if self.skill_level != 'any' else query_parts.append("_")
        # Placeholder for time, as it's always 'all_day'
        query_parts.append("_")
        query_parts.append(
            f"'{self.indoor_outdoor}'") if self.indoor_outdoor != 'any' else query_parts.append("_")

        return "recommend_facility({}, {}, {}, {}, Facility)".format(*query_parts)

    def extract_info(self, doc):
        # Improved extraction logic to better handle 'any' or specific values
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

        return sport, location


def main():
    app = QApplication(sys.argv)
    ex = ExpertSystemGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
