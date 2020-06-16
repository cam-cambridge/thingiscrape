# Thingiscrape
Thingiverse REST API python wrapper

## About <a name = "about"></a>
A python based [Thingiverse.com](https://www.thingiverse.com) object scraper and downloader. The program can search of objects using keywords, licenses, users, categories and then sort the results, for example returning the most popular or newest uploads.

## Getting Started <a name = "getting_started"></a>

First you need to install the requirements - there are not that many 😊.
```
pip install -r requirements.txt
```

You need to add an environment variable containing the Thingiscrape applications API token.
Contact [@dougbrion](https://github.com/dougbrion) [dajb3@cam.ac.uk](mailto:dajb3@cam.ac.uk) to get the token or create your own Thingiverse application by visiting the following site: [https://www.thingiverse.com/apps](https://www.thingiverse.com/apps)

```
export API_TOKEN "<your-api-token>"
```

## Usage <a name = "usage"></a>

To see the various options available to you type the following into your terminal.

```
python thingiscrape.py --help
```

Example usage:

```
python thingiscrape.py --search "yoda" --popular 1 --pages 2 --license "cc"
```

STL 3D model files will be downloaded to `./downloads/stls/` along with a json file containing the results from the request in `./downloads/json/`.