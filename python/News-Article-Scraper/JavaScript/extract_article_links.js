const cheerio = require("cheerio");
const axios = require("axios");
url = `https://www.patrika.com/googlenewssitemap1.xml`;
let links = [];
async function getLinks() {
    try {
        const response = await axios.get(url);
        const $ = cheerio.load(response.data, { xmlMode: true });
        all_loc = $('loc')
        all_loc.each(function () {
            links.push($(this).text())
        })
        console.log(links.length + ' links found.')

    } catch (error) {
        console.error(error);
    }
}
getLinks();
