# NeuronautLLM-database

A series of scripts and documentation to aid in setting up a neuron database for NeuronautLLM

## Fetching data

*Fetching neuron explainer data from OpenAI's Azure blob storage.*

Use the `get_neuron_explainer_dataset.py` python script to retrieve the GPT-2 small neuron data. Some files may not be successfully fetched, so the script can be safely run multiple times until all files have been successfully downloaded.

Within the `get_neuron_explainer_dataset.py` file are the following values that can changed the script's behaviour:

- `data_sources`: Tell the script where to fetch neuron activation data from.
- `DISABLE_OVERWRITE`: Set to `True` if you want to avoid redownloading and overwriting files that have already been fetched.
- `REQUEST_POOL_SIZE`: The number of requests that will be handled at a time, can be adjusted to improve download time.
- `N_REQUESTS_BETWEEN_PROGRESS_REPORTS`: How often to report download progress.

## Importing data to database

*Taking the fetched neuron data and importing some parts of it into a SQLite3 database.*

First, initialize the SQLite3 database with the `ChinaGraph2024-gpt2small-init.session.sql` file. The schema for the data can be found at `ChinaGraph2024-gpt2small-db-schema.png`.

Secondly, use the `import_neuron_explainer_data_to_database.ipynb` Jupyter Notebook to import the locally stored fetched data into a new SQLite3 database.

Finally, perform clusting and classification of neurons with `bertopic_params.ipynb`.
