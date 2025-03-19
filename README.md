# ArtSearch

## Download Elasticsearch engine

Download Elasticsearch engine:

```bash
cd data
wget -O elasticsearch-8.17.3.tar.gz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.17.3-linux-x86_64.tar.gz  # download Elasticsearch
tar zxvf elasticsearch-8.17.3.tar.gz
rm elasticsearch-8.17.3.tar.gz 
cd ..
```

## Download Wikipedia data

Download Wikipedia data with a specific language.

For example, English Wikipedia data (default language) 20231101 (latest) version data can be downloaded with the following command:

```bash
modelscope download --dataset wikimedia/wikipedia --include 20231101.en/* --local_dir ./data/wikipedia
```

An example of the Wikipedia data looks as follows:

```json
{
    "id": "1",
    "url": "https://simple.wikipedia.org/wiki/April",
    "title": "April",
    "text": "April is the fourth month..."
}
```

## Build index

Build index for the Wikipedia data:

```bash
python es_wiki_build.py
python es_wiki_build.py --language en
```

## Search

Search for the query:

```bash
python es_wiki_search.py
python es_wiki_search.py --language en --query "Paris 2024 Olympic Games"
```