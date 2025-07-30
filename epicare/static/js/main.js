// Form validation, dark mode, and quiz logic
document.addEventListener('DOMContentLoaded', () => {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let valid = true;
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('border-red-500');
                } else {
                    input.classList.remove('border-red-500');
                }
            });
            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
});

// Quiz state for Alpine.js
function quizState() {
    return {
        currentQuestion: 0,
        showResult: [],
        isCorrect: [],
        questions: [
            {
                text: "What is the first step in helping someone having a seizure?",
                options: ["Put something in their mouth", "Move them to a safe area", "Call for emergency help immediately", "Restrain them"],
                correct: "Move them to a safe area",
                explanation: "Clear the area of hazards and ensure their safety."
            },
            {
                text: "Can epilepsy be treated?",
                options: ["Yes", "No", "Only in children", "Only with surgery"],
                correct: "Yes",
                explanation: "Epilepsy can often be managed with medication or other treatments."
            }
        ],
        selectAnswer(index, option) {
            this.showResult[index] = true;
            this.isCorrect[index] = option === this.questions[index].correct;
        },
        nextQuestion() {
            if (this.showResult[this.currentQuestion]) {
                this.currentQuestion++;
            }
        },
        resetQuiz() {
            this.currentQuestion = 0;
            this.showResult = [];
            this.isCorrect = [];
        }
    };
}