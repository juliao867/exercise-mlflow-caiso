# CAISO MLflow model

For those of you using conda, make sure to switch the line python_env: python_env.yaml in the MLProject file to python_env: conda.yaml.


California ISO Model for load forecasting (CAISO): It predicts for the next
day by taking hourly averages of the three days with highest
average consumption value among a pool of ten previous days,
excluding weekends, holidays, and past DR event days

Tho model is packed as a MLflow Project. When run, it fetches the newest data, trains a CAISO model and saves it locally as an MLflow Model. 
Here's a starting point for running and deploying a CAISO model locally:

```
git clone https://github.itu.dk/Big-Data-Management-2025/caiso-mlflow
cd caiso-mlflow
mlflow run .
mlflow models serve -m model
```

You can now query the model using curl, for example:
```
curl http://127.0.0.1:5000/invocations -H 'Content-Type: application/json' -d '{"dataframe_records":[{"Time":"2025-01-10T15:0:00Z"}]}'
```
Alternatively, you can download an extension in VS Code, called "Thunder Client", which gives you a nicer way how to send request. Just simply go to Extensions in VS Code, search for "Thunder Client" (has a purple icon) and install it.  
Then select POST and enter this url: http://127.0.0.1:5000/invocations.  
Select JSON and input this text:  
```
{"dataframe_split":{"columns": ["Time"],"data":[["2025-01-10T15:00:00"]]}}
```  
Hit the blue button "Send", and when successful, you should see an output similar to the one below:  

<img width="1149" alt="image" src="https://github.itu.dk/storage/user/5272/files/37aad830-0007-41be-aabc-9c977a5300d2">
