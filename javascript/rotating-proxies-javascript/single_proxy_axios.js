// Import axios
const axios = require("axios");

// Create and execute a new Promise
(async function () {
    try {

        // Proxy with authentication
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
        const url = `https://httpbin.org/ip`;
        
        // Call the GET method on the URL with proxy information
        const response = await axios.get(url, {
            proxy: proxy_no_auth
        });
        // Print effective IP address
        console.log(response.data);
    } catch (err) {

        //Log the error message
        console.error(err);
    }
})();

