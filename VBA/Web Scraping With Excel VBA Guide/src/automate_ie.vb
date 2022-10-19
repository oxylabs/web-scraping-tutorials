Sub scrape_quotes()
    Dim browser As InternetExplorer
    Dim page As HTMLDocument
    Set browser = New InternetExplorer
    browser.Visible = True
    browser.navigate ("https://quotes.toscrape.com")
End Sub