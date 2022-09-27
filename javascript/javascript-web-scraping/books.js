const fs = require("fs");
const j2cp = require("json2csv").Parser;
const axios = require("axios");
const cheerio = require("cheerio");
 
const mystery = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html";
 
const books_data = [];
 
async function getBooks(url) {
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);
 
    const books = $("article");
    books.each(function () {
      title = $(this).find("h3 a").text();
      price = $(this).find(".price_color").text();
      stock = $(this).find(".availability").text().trim();
      books_data.push({ title, price, stock });
    });
    // console.log(books_data);
    const baseUrl = "http://books.toscrape.com/catalogue/category/books/mystery_3/";
    if ($(".next a").length > 0) {
      next = baseUrl + $(".next a").attr("href");
      getBooks(next);
    } else {
      const parser = new j2cp();
      const csv = parser.parse(books_data);
      fs.writeFileSync("./books.csv", csv);
    }
  } catch (err) {
    console.error(err);
  }
}
 
getBooks(mystery);