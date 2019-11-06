import json
import pandas as pd
import boto3 as bt3
import re
    
def lambda_handler(event, context):
    
    s3 = bt3.client('s3')
    method = event.get('httpMethod',{})
    
    with open('index.html', 'r') as f:
        indexPage = f.read()
        
    status_check = [0]*10 
        
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
            'Content-Type': 'text/html',
            },
            "body": indexPage
        }
        
    if method == 'POST':
        bodyContent = event.get('body',{}) 
        parsedBodyContent = json.loads(bodyContent)
        testCases = re.sub('&zwnj;.*&zwnj;','',parsedBodyContent["shown"]["0"], flags=re.DOTALL)
        questionName = parsedBodyContent["qname"]["0"]
        userSolution = parsedBodyContent["editable"]["0"] 
        
        # Reading the original dataframe from S3 
        original_df = pd.read_csv('https://frame-pandas.s3.amazonaws.com/pandas_data.csv')
        default_df = original_df.copy()
        
        # Evaluating User Inputs
        user_list = userSolution.splitlines()
        user_list = [x for x in user_list if not x.startswith('#')]
        for i in user_list:
            original_df = pd.eval(i)
        # if isinstance(user_output_df, pd.core.series.Series):
        #    user_output_df = user_output_df.to_frame()
        userHtmlFeedback = original_df.to_html()
        
        # Question 5
        isComplete = 0
        right_answer = default_df[default_df['CHILDREN']=='Yes']
        right_answer_text = 'original_df[original_df[\'CHILDREN\']==\'Yes\']'
        if right_answer.equals(original_df):
            status_check[4]=1
            isComplete = 1

        progress = len([qn for qn in status_check if qn == 5])
        
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
                },
            "body":  json.dumps({
                "isComplete":isComplete,
                "pythonFeedback": "Hello",
                "htmlFeedback": userHtmlFeedback,
                "textFeedback": right_answer_text,
                "progress": progress,
                "questionStatus":status_check
            })
        }
