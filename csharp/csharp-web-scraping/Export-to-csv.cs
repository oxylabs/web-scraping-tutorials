static void exportToCSV(List<Book> books)
{
    using (var writer = new StreamWriter("./books.csv"))
    using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
    {
        csv.WriteRecords(books);
    }
}