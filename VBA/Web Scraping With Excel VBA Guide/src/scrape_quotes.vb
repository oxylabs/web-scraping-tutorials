Sub scrape_quotes()
    Dim browser As InternetExplorer
    Dim page As HTMLDocument
    Dim quotes As Object
    Dim authors As Object
    
    Set browser = New InternetExplorer
    browser.Visible = True
    browser.navigate ("https://quotes.toscrape.com")
    Do While browser.Busy: Loop
    
    Set page = browser.document
    Set quotes = page.getElementsByClassName("quote")
    Set authors = page.getElementsByClassName("author")
    
    For num = 1 To 5
        Cells(num, 1).Value = quotes.Item(num).innerText
        Cells(num, 2).Value = authors.Item(num).innerText
    Next num
    
    browser.Quit
End Sub
