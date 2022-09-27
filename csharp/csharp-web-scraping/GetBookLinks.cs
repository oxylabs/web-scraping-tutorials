static List<string> GetBookLinks(string url)
    {
        var bookLinks = new List<string>();
        HtmlDocument doc = GetDocument(url);
        HtmlNodeCollection linkNodes = doc.DocumentNode.SelectNodes("//h3/a");
        var baseUri = new Uri(url);
        foreach (var link in linkNodes)
        {
            string href = link.Attributes["href"].Value;
            bookLinks.Add(new Uri(baseUri, href).AbsoluteUri);
        }
        return bookLinks;
    }