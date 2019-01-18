// grab reference to question
let survey_question = document.getElementsByClassName("surveyQuestion");

// make question data frame
let question_data = {
    "question" : "",
    "type" : "",
    "answers" : []
};

// make template for answers
let answer_template = {
    "text" : "",
    "data-value" : null
};

// if our reference is valid
if (survey_question.length) {
    // we extract the question from its container
    survey_question = survey_question[0];

    // assign question text from page value
    question_data["question"] = survey_question.getElementsByClassName("surveyQuestionText")[0].innerText;

    // grab answer options
    let answer_options = survey_question.getElementsByClassName("questionDropdownOptions");

    if (answer_options.classList.contains("activeSelectMenu")) {
        question_data["type"] = 'checkbox';
    } else {
        question_data["type"] = 'select'

    }

    // if reference is valid
    if (answer_options.length) {

        // grab answer options
        answer_options = Array.from(answer_options[0].getElementsByTagName("span"));

        // add each answer to the data frame
        answer_options.forEach(option => {
            // make sure to copy template, not grab reference
            let current_answer = Object.assign({}, answer_template);

            // assign values from page
            current_answer["text"] = option.innerText;
            current_answer["data-value"] = option.getAttribute("data-value");

            // push current answer to data frame
            question_data["answers"].push(current_answer);
        });
    }
}

// noinspection JSAnnotator
return question_data;