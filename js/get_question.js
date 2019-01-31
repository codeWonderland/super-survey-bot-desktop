// grab reference to question
let survey_question = document.getElementsByClassName("surveyQuestion");

// make question data frame
let question_data = {
    "QUESTION" : "",
    "TYPE" : "",
    "ANSWERS" : []
};

// make template for answers
let answer_template = {
    "TEXT" : "",
    "data-value" : null
};

// if our reference is valid
if (survey_question.length) {
    // we extract the question from its container
    survey_question = survey_question[0];

    // assign question text from page value
    question_data["QUESTION"] = survey_question.getElementsByClassName("surveyQuestionText")[0].innerText;

    // grab answer options
    let answer_options = survey_question.getElementsByClassName("questionDropdownOptions");



    // if reference is valid
    if (answer_options.length) {

        // check answer options for type of question
    if (answer_options[0].classList.contains("activeSelectMenu")) {
        question_data["TYPE"] = 'CHECKBOX';

    } else {
        question_data["TYPE"] = 'SELECT'
    }

        // grab answer options
        answer_options = Array.from(answer_options[0].getElementsByTagName("span"));

        // add each answer to the data frame
        answer_options.forEach(option => {
            // make sure to copy template, not grab reference
            let current_answer = Object.assign({}, answer_template);

            // assign values from page
            current_answer["TEXT"] = option.innerText;
            current_answer["DATA_VALUE"] = option.getAttribute("data-value");

            // push current answer to data frame
            question_data["ANSWERS"].push(current_answer);
        });
    }
}

// noinspection JSAnnotator
return question_data;