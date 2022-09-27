const cheerio = require("cheerio");
const axios = require("axios");
url = `https://www.example.com/sitemap.xml`;
let links = [];
async function getLinks() {
    try {
        const response = await axios.get(url);
        const $ = cheerio.load(response.data, { xmlMode: true });
        all_loc = $('loc');
        all_loc.each(function () {
            links.push($(this).text());
        })
        console.log(links.length + ' links found.');
        links.forEach(async function (story_link) {
            try {
                let story = await axios.get(story_link);
                let $ = cheerio.load(story.data);
                heading = $('h1').text()
                body = $('.complete-story p').text()

            } catch (error) {
                console.error('internal\n' + error)
            }
        })

    } catch (error) {
        console.error(error);
    }
}
getLinks();
