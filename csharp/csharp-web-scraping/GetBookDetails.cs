static List<Book> GetBookDetails(List<string> urls)
{
    var books = new List<Book>();
    foreach (var url in urls)
    {
        HtmlDocument document = GetDocument(url);
        var titleXPath = "//h1";
        var priceXPath = "//div[contains(@class,\"product_main\")]/p[@class=\"price_color\"]";
        var book = new Book();
        book.Title = document.DocumentNode.SelectSingleNode(titleXPath).InnerText;
        book.Price = document.DocumentNode.SelectSingleNode(priceXPath).InnerText;
        books.Add(book);
    }
    return books;
}