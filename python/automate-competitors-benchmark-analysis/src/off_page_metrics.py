import time
from mozscape import Mozscape

client = Mozscape("<MOZ username>", "<MOZ password>")

for y in list_comparison:
    try:
        print("Getting MOZ results for: " + y[0])
        domainAuthority = client.urlMetrics(y[0])
        y.extend([domainAuthority["ueid"], domainAuthority["uid"], domainAuthority["pda"]])
    except Exception as e:
        print(e)
        time.sleep(10)  # Retry once after 10 seconds.
        domainAuthority = client.urlMetrics(y[0])
        y.extend([domainAuthority["ueid"], domainAuthority["uid"], domainAuthority["pda"]])