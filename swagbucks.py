from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


def start_crawl(driver: WebDriver):
    """
    The first interaction we have with any quiz is data verification
    
    We start with a question on DOB
    
    The question is wrapped in a div.question-container
    
    The question text is in div.question
    
    There are three entry fields:
    div#dob2_m.questionDropdownContainer
    div#dob2_d.questionDropdownContainer
    div#dob2_y.questionDropdownContainer
    
    the structure of the answer fields are as follows
    
    div.questionDropdownContainer
    └─span.questionDropdownPlaceholder[data-val] - where data-val needs to be updated with the answer id
    └─div.questionDropdownOptions
      └─span[class^=option][data-id] - where the data-id is the answer id and the answer is the innerText. 
    └─input[value] - where value is updated with the answer id 
    
    As far as I can tell, the only part of this that actually matters is the input value
    
    Following the DOB question, there will be another data verification question,
    this time about the user's gender
    
    unlike before, where the question was a dropdown box, this time we have radio buttons to select from
    
    question structure:
    
    div.question-container
    └─div.question - question is innerText
    └─div.answer
      └─div.options
      
    option structure:
    
    label.radio
    └─input[type="radio"][value] - where value is the answer id
    └─span - where innerText is the answer text
    
    unlick with dropdowns, it is easier to check the value of the 
    button via the span tag then click() either the label or the span tag
    
    we have one more radio entry question, the number of people in your household
    
    Following this, we go into the main survey
    
    the main survey usually gets thrown to http://swagbucks.qs1.sgizmo.com
    
    this site will test to make sure we are not a bot
    
    following this test we get thrown to individual company's sites
    """


def getRadioAnswers():
    """Get radio answer options
    question structure:

    div.question-container
    └─div.question - question is innerText
    └─div.answer
      └─div.options

    option structure:

    label.radio
    └─input[type="radio"][value] - where value is the answer id
    └─span - where innerText is the answer text

    unlick with dropdowns, it is easier to check the value of the
    button via the span tag then click() either the label or the span tag

    :return: dict{answer_id: answer_value}
    """

def calcCurrency():
    """
    500 SB = 5 USD

    if we answer a question from the side thing every 3 seconds,
    we will make 10 USD in 52 min || 11.52 USD per hour

    :return:
    """