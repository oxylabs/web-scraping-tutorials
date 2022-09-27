import io
import pathlib
import hashlib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver


def get_content_from_url(url):
   driver = webdriver.Chrome()  # add "executable_path=" if driver not in running directory
   driver.get(url)
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   page_content = driver.page_source
   driver.quit()  # We do not need the browser instance for further steps.
   return page_content


def parse_image_urls(content, classes, location, source):
   soup = BeautifulSoup(content)
   results = []
   for a in soup.findAll(attrs={"class": classes}):
       name = a.find(location)
       if name not in results:
           results.append(name.get(source))
   return results


def save_urls_to_csv(image_urls):
   df = pd.DataFrame({"links": image_urls})
   df.to_csv("links.csv", index=False, encoding="utf-8")


def get_and_save_image_to_file(image_url, output_dir):
   response = requests.get(image_url, headers={"User-agent": "Mozilla/5.0"})
   image_content = response.content
   image_file = io.BytesIO(image_content)
   image = Image.open(image_file).convert("RGB")
   filename = hashlib.sha1(image_content).hexdigest()[:10] + ".png"
   file_path = output_dir / filename
   image.save(file_path, "PNG", quality=80)


def main():
   url = "https://your.url/here?yes=brilliant"
   content = get_content_from_url(url)
   image_urls = parse_image_urls(
       content=content, classes="blog-card__link", location="img", source="src",
   )
   save_urls_to_csv(image_urls)

   for image_url in image_urls:
       get_and_save_image_to_file(
           image_url, output_dir=pathlib.Path("nix/path/to/test"),
       )


if __name__ == "__main__":  #only executes if imported as main file
   main()