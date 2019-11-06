import json
import pandas as pd
import boto3 as bt3
import re

status_check = [0]*10    
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
        questionName = parsedBodyContent["qname"]["0"]
        original_df = pd.read_csv('https://frame-pandas.s3.amazonaws.com/pandas_data.csv')
        user_output_df = pd.eval(userSolution)
        userHtmlFeedback = user_output_df.to_html()
        right_answer_text = "temp"
        isComplete = 0
        if questionName == 'Selecting Rows':#Q1
            right_answer = original_df.iloc[[1,4,9]]
            right_answer_text = 'original_df.iloc[[1,4,9]]'
            if(right_answer.equals(user_output_df)):
                status_check[0]=1
                isComplete = 1
        elif questionName == 'Selecting Columns':#Q2
            right_answer = original_df[['ID','NAME','RESIDENCE']]
            right_answer_text = 'original_df[[\'ID\',\'NAME\',\'RESIDENCE\']]'
            if(right_answer.equals(user_output_df)):
                status_check[1]=1
                isComplete = 1
        elif questionName == 'Selecting Specific Cells':#Q3
            right_answer = original_df.iloc[8]['NAME']
            right_answer_text = 'original_df.iloc[8][\'NAME\']'
            if(right_answer.equals(user_output_df)):
                status_check[2]=1
                isComplete = 1
        elif questionName == 'Renaming Column Names':#Q4
            right_answer = original_df.rename({'GENDER':'SEX','RESIDENCE':'ZOO'})
            right_answer_text = 'original_df.rename({\'GENDER\':\'SEX\',\'RESIDENCE\':\'ZOO\'})'
            if(right_answer.equals(user_output_df)):
                status_check[3]=1
                isComplete = 1
        elif questionName == 'Filtering Data in Columns':#Q5
            right_answer = original_df[original_df['CHILDREN']=='Yes']
            right_answer_text = 'original_df[original_df[\'CHILDREN\']==\'Yes\']'
            if(right_answer.equals(user_output_df)):
                status_check[4]=1
                isComplete = 1
        elif questionName == 'Filtering Data based on Multiple Conditions':#Q6
            right_answer = original_df[(original_df['CHILDREN']=='Yes')|(original_df['RESIDENCE']=='China')]
            right_answer_text = 'original_df[(original_df[\'CHILDREN\']==\'Yes\')|(original_df[\'RESIDENCE\']==\'China\')]'
            if(right_answer.equals(user_output_df)):
                status_check[5]=1
                isComplete = 1
        elif questionName == 'Adding New Rows':#Q7
            right_answer = original_df.append(pd.Series([11,'Tao Tao', 'M', 20, 'No', 'China'], index=original_df.columns), ignore_index=True)
            right_answer_text = 'original_df.append(pd.Series([11,\'Tao Tao\', \'M\', 20, \'No\', \'China\'], index=original_df.columns), ignore_index=True)'
            if(right_answer.equals(user_output_df)):
                status_check[6]=1
                isComplete = 1
        elif questionName == 'Using Min and Max':#Q9
            right_answer = original_df.min(axis = 1)
            right_answer_text = 'original_df.min(axis = 1)'
            if(right_answer.equals(user_output_df)):
                status_check[8]=1
                isComplete = 1
        elif questionName == 'Multiplying and Dividing Column values':#Q10
            right_answer = 10*original_df.iloc[:,3]
            right_answer_text = '10*original_df.iloc[:,3]'
            if(right_answer.equals(user_output_df)):
                status_check[9]=1
                isComplete = 1
        
                


        progress = status_check.count(1)
        print(status_check)
        print(progress)
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
