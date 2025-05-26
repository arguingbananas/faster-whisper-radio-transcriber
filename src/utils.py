def setup_logging(log_file='transcriber.log'):
    import logging

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def download_audio(url, output_path):
    import requests

    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download audio from {url}. Status code: {response.status_code}")