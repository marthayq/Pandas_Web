import json
import pandas as pd
import boto3 as bt3
import re
    
def lambda_handler(event, context):
    
    s3 = bt3.client('s3')
    
    #csv_data_1 = s3.get_object(Bucket='frame-pandas', Key='Pandas_Q1.csv')
    #print('CSV', csv_data_1)
    #contents_1 = csv_data_1['Body'].read()
    #print('Body', contents_1)
    
    method = event.get('httpMethod',{}) 
    
    with open('index.html', 'r') as f:
        indexPage = f.read()
        
    
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
        userSolution = parsedBodyContent["editable"]["0"] 
        
        original_df = pd.read_csv('https://frame-pandas.s3.amazonaws.com/pandas_data.csv')
        print("Original Df", original_df)
        
        print("User Solution", userSolution)
        user_output_df = pd.eval(userSolution)
        print("Big Problem", type(user_output_df))
        print("Testing Output", user_output_df)
        userHtmlFeedback = user_output_df.to_html()
        
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
                },
            "body":  json.dumps({
                "isComplete":"Hello",
                "pythonFeedback": "Hello",
                "htmlFeedback": userHtmlFeedback,
                "textFeedback": "Hello"
            })
        }
