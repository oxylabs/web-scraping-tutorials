const csv = require('async-csv');
const fs = require('fs').promises;
const axios = require("axios");

(async () => {
    // Read file from disk:
    const csvFile = await fs.readFile('proxy_list.csv');

    // Convert CSV string into rows:
    const data = await csv.parse(csvFile);
    await Promise.all(data.map(async (item) => {
        try {

            // Create the Proxy object
            proxy_no_auth = {
                host: '206.253.164.122',
                port: 80
            }

            // Proxy with authentication
            proxy_with_auth = {
                host: '46.138.246.248',
                port: 8088,
                auth: {
                    username: 'USERNAME',
                    password: 'PASSWORD'
                }
            }

            // This URL returns the IP
            const url = `https://httpbin.org/ip`;

            // Call the GET method on the URL with proxy information
            const response = await axios.get(url, {
                proxy: proxy_no_auth
            });
            // Print effective IP address
            console.log(response.data);
        } catch (err) {

            // Log failed proxy
            console.log('Proxy Failed: ' + item[0]);
        }
    }));

})();
