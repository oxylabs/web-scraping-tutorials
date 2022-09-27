// import axios
const axios = require("axios");

// Creaet and execute a new Promise
(async function () {
    try {
        // This URL returns the IP address
        const url = `https://httpbin.org/ip`;

        // call the GET method on the URL
        const response = await axios.get(url);

        // print the response data, which is the IP address
        console.log(response.data);
    } catch (err) {

        // print the error message
        console.error(err);
    }
})();

