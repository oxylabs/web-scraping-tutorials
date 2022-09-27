const fs = require("fs");
const j2cp = require("json2csv").Parser;
const axios = require("axios");
const cheerio = require("cheerio");

const wiki_python =  "https://en.wikipedia.org/wiki/Python_(programming_language)";

async function getWikiTOC(url) {
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);

    const TOC = $("li.toclevel-1");
    let toc_data = [];
    TOC.each(function () {
      level = $(this).find("span.tocnumber").first().text();
      text = $(this).find("span.toctext").first().text();
      toc_data.push({ level, text });
    });
    const parser = new j2cp();
    const csv = parser.parse(toc_data);
    fs.writeFileSync("./wiki_toc.csv", csv);
  } catch (err) {
    console.error(err);
  }
}

getWikiTOC(wiki_python);
