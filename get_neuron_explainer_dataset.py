#!/usr/bin/env python
import os
import grequests
import requests
import urllib

data_sources = [
  {
    "name": "activations",
    "model": "gpt2-small",
    "n_layers": 12,
    "n_neurons_per_layer": 3072,
    "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/gpt2_small_data/collated-activations/{layer_index}/{neuron_index}.json",
  },
  {
    "name": "explanations",
    "model": "gpt2-small",
    "n_layers": 12,
    "n_neurons_per_layer": 3072,
    "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/gpt2_small_data/explanations/{layer_index}/{neuron_index}.jsonl",
  },
  {
    "name": "activations",
    "model": "gpt2-small",
    "n_layers": 12,
    "n_neurons_per_layer": 3072,
    "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/gpt2_small_data/collated-activations/{layer_index}/{neuron_index}.json",
  },
  {
    "name": "explanations",
    "model": "gpt2-small",
    "n_layers": 12,
    "n_neurons_per_layer": 3072,
    "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/gpt2_small_data/explanations/{layer_index}/{neuron_index}.jsonl",
  },
  # {
  #   "name": "activations",
  #   "model": "gpt2-xl",
  #   "n_layers": 48,
  #   "n_neurons_per_layer": 6400,
  #   "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/data/collated-activations/{layer_index}/{neuron_index}.json",
  # },
  # {
  #   "name": "explanations",
  #   "model": "gpt2-xl",
  #   "n_layers": 48,
  #   "n_neurons_per_layer": 6400,
  #   "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/data/explanations/{layer_index}/{neuron_index}.jsonl",
  # },
  # {
  #   "name": "weight-related-neurons",
  #   "model": "gpt2-xl",
  #   "n_layers": 48,
  #   "n_neurons_per_layer": 6400,
  #   "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/data/related-neurons/weight-based/{layer_index}/{neuron_index}.json",
  # },
  # {
  #   "name": "activation-related-tokens",
  #   "model": "gpt2-xl",
  #   "n_layers": 48,
  #   "n_neurons_per_layer": 6400,
  #   "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/data/related-tokens/activation-based/{layer_index}/{neuron_index}.json",
  # },
  # {
  #   "name": "weight-related-tokens",
  #   "model": "gpt2-xl",
  #   "n_layers": 48,
  #   "n_neurons_per_layer": 6400,
  #   "url_pattern": "https://openaipublic.blob.core.windows.net/neuron-explainer/data/related-tokens/weight-based/{layer_index}/{neuron_index}.json",
  # }
]

DISABLE_OVERWRITE = True
REQUEST_POOL_SIZE = 10
N_REQUESTS_BETWEEN_PROGRESS_REPORTS = 100

def remove_urls_where_file_exists(urls, model_name, resource_category, layer_index):
  for url in urls.copy():
    file_name = url.split("/")[-1]
    file_path = "./data/{}/{}/{}/{}".format(model_name, resource_category, layer_index, file_name)
    if os.path.exists(file_path):
      urls.remove(url)
  
  return urls

def save_data_to_file(data, file_name, file_dir="./data/"):
  with open(file_dir + file_name, 'wb') as out_file:
    out_file.write(data)
  
def handle_response(response, model_name, resource_category, layer_index, neuron_index):
  if response is None or response.status_code != 200:
    print("Failed to get {} @ layer {}, neuron {}".format(resource_category, layer_index, neuron_index))
    return
    
  file_name = urllib.parse.urlparse(response.url).path.split('/')[-1]
  file_dir = "./data/{}/{}/{}/".format(model_name, resource_category, layer_index)
  save_data_to_file(response.content, file_name, file_dir)
  
def print_estimated_time_remaining(previous_layer_download_duration, n_layers_remaining):
  if previous_layer_download_duration is None:
    return
  estimated_time_remaining = previous_layer_download_duration * n_layers_remaining
  print("Estimated time remaining: {} seconds".format(estimated_time_remaining))

if __name__ == "__main__":  
  for source_index, source in enumerate(data_sources):
    for layer_index in range(source["n_layers"]):
      # make dir for this layer
      os.makedirs("./data/{}/{}/{}/".format(source["model"], source["name"], layer_index), exist_ok=True)
      
      # build all URLs for this layer
      urls = [
        source["url_pattern"].format(layer_index=layer_index, neuron_index=neuron_index) 
        for neuron_index in range(source["n_neurons_per_layer"])
      ]
      
      if DISABLE_OVERWRITE:
        urls = remove_urls_where_file_exists(urls, source["model"], source["name"], layer_index)
        if len(urls) == 0:
          print("Skipping {} for layer {}/{} as all files are present".format(source["name"], layer_index, source["n_layers"]))
          continue
        elif len(urls) < source["n_neurons_per_layer"]:
          print("{}/{} files found for {} in layer {}/{}, will download the remaining {}".format(
            source["n_neurons_per_layer"] - len(urls), 
            source["n_neurons_per_layer"], 
            source["name"], 
            layer_index, 
            source["n_layers"],
            len(urls),
          ))
        else:
          print("Downloading {} for layer {}/{}".format(source["name"], layer_index, source["n_layers"]))
      
      # create requests
      requests = (grequests.get(url) for url in urls)
      
      
      # send requests
      for url_index, response in grequests.imap_enumerated(requests, size=REQUEST_POOL_SIZE):
        if (url_index + 1) % N_REQUESTS_BETWEEN_PROGRESS_REPORTS == 0:
          print("Processed {}/{} of neuron {} for layer {}".format(url_index + 1, len(urls), source["name"], layer_index))
        
        neuron_index = urls[url_index].split("/")[-1].split(".")[0]
        handle_response(response, source["model"], source["name"], layer_index, neuron_index)