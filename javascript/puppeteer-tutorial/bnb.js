const puppeteer = require("puppeteer");
(async () => {
  let url = "https://www.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&search_type=section_navigation&property_type_id%5B%5D=8";
  const browser = await puppeteer.launch(url);
  const page = await browser.newPage();
  await page.goto(url);
  data = await page.evaluate(() => {
    root = Array.from(document.querySelectorAll("#FMP-target [itemprop='itemListElement']"));
    hotels = root.map(hotel => ({
      Name: hotel.querySelector('ol').parentElement.nextElementSibling.textContent,
      Photo: hotel.querySelector("img").getAttribute("src")
    }));
    return hotels;
  });
  console.log(data);
  await browser.close();
})();