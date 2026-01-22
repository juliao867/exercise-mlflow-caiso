# CAISO MLflow model

California ISO Model for load forecasting (CAISO): predicts the electricity load for the next
day by taking hourly averages of the three days with highest average consumption value among a pool of ten previous days, excluding weekends, holidays, and past DR event days.

With the help of this example you will learn how to use a real-world electricity load forecasting model packaged as an MLflow Project, how to log and save a model, and serve it locally as a REST API that can be queried.

First click **Use this template** and then **create a codespace** for the project (click <> Code then Codespaces).

Once the codespace finished building, navigate to the terminal and **install MLflow**:

```
pip install mlflow
```

MLflow will be installed in a local environment associated with the current codespace.
> Note: MLflow could also be listed in requirements.txt and installed automatically when the codespace is created. In this exercise, we install it manually to ensure the `mlflow` command is available without additional PATH configuration.

Now let's have a look at the files in the Explorer tab. `CAISO.py` is the script you will use to run the model packaged in this project. Make sure you understand what it does. The files `custom_transformers.py` and `prepos.py` are simply helper files for preprocessing the data. 

The `MLproject` file gives MLflow instructions for how to run this project. In our case it mentions the name of the project, the environment file that contains the dependencies needed to run the project, and instructions on how to run the model. In this case we simply need to run the `CAISO.py` python file without any arguments.

In this way the model is packaged as a MLflow Project. When the project is ran it trains a CAISO model, logs the training error, and saves the model as a python function.

First, inside the terminal run the MLflow project with:

```
mlflow run . --env-manager local
```

Here we are telling MLflow that it should use the local environment. If you were running this code locally, on your machine, inside a conda environment, you wouldn't have to add `--env-manager local`, but simply run `mlflow run .` In this case you would need to make a change to the `MLproject` file - do you know what that is?

Back to our example, the model should be trained and you should see in the terminal the MAE, r2 score, and that the model was successfully saved. You might notice a few new files and folders were created; for example the `model` contains the model (as a `.pkl` file) and the dependencies needed to create this model.

We can now serve the model to test if it can generate new predictions. This is an important step before deployment. In the terminal type:

```
mlflow models serve -m model --env-manager local
```

In the terminal you will see the address where a web server is listening to requests:  `INFO: Uvicorn running on http://127.0.0.1:5000`. `127.0.0.1` is a loopback address (localhost) which means _only accessible from this machine_. `:5000` is the port number which identifies which service on the machine should receive the request. 

You can now query the model using curl and the above address. In a _different terminal_ run for example:
```
curl http://127.0.0.1:5000/invocations -H 'Content-Type: application/json' -d '{"dataframe_records":[{"Time":"2026-01-01T15:0:00Z"}]}'
```
which will print the output: `{"predictions": [27.709061405555556]}`. 

The above command explained:

* `curl` - send an HTTP request to a given address and print the response to the terminal 
* `http://127.0.0.1:5000/invocations` - send a request to the local server where the model is running, using the `invocantions` endpoint because we are requesting predictions
* `'Content-Type: application/json'` - data will be sent in a json format
* `-d '{"dataframe_records":[{"Time":"2026-01-01T15:0:00Z"}]}'` - sends input data in the request body
* `dataframe_records` tells MLflow to interpret the input as rows of a pandas DataFrame, where each JSON object corresponds to one row.
