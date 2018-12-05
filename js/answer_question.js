// grab a reference to the question in question
let survey_question = document.getElementsByClassName("surveyQuestion");

// if the reference is valid
if (survey_question.length) {
    // we extract the element from it's container
    survey_question = survey_question[0];

    // grab all answer options
    let answer_options = survey_question.getElementsByClassName("questionDropdownOptions");

    // if our reference is valid
    if (answer_options.length) {
        // we make an array from the span elements with the answers in them
        answer_options = Array.from(answer_options[0].getElementsByTagName("span"));

        // select answers on the page that match user answers
        answer_options.forEach(option => {
            // answers come as csv
            arguments[0].split(',')
                .forEach(user_answer => {
                    if (user_answer === option.getAttribute("data-value")) {
                        option.click();
                    }
                });
        });

        // swagbucks function to save answer
        sp.saveAnswer();
    }
}