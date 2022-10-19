# Enable Proxy
export http_proxy="http://user:pwd@127.0.0.1:1234"
export https_proxy="http://user:pwd@127.0.0.1:1234"

curl "http://httpbin.org/ip"

# Disable proxy
unset http_proxy
unset https_proxy