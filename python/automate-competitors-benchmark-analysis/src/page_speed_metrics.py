import json

pagespeed_key = "<your page speed key>"


for y in list_comparison:
    try:

        print("Getting results for: " + y[0])
        url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + y[0] + "&strategy=mobile&locale=en&key=" + pagespeed_key
        response = requests.request("GET", url)
        data = response.json() 

        overall_score = data["lighthouseResult"]["categories"]["performance"]["score"] * 100
        fcp = data["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
        fid = data["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["percentile"]/1000
        lcp = data["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]
        cls = data["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100



        y.extend([fcp, fid, lcp, cls, overall_score])

    except Exception as e:
        print(e)
        y.extend(["No data", "No data", "No data", "No data", overall_score])