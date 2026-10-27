// Selected historical excerpt; imports, surrounding class and other logic omitted.
// Documentation sample only: not a complete buildable application.

    CancellationToken cancellationToken = default)
        {
            const string sql = """
        DECLARE @Today date = CONVERT(date, GETDATE());

        WITH Days AS
        (
            SELECT DATEADD(day, -v.n, @Today) AS [Date]
            FROM (VALUES (6), (5), (4), (3), (2), (1), (0)) v(n)
        )
        SELECT
            d.[Date],
            COUNT(p.id) AS [Count]
        FROM Days d
        LEFT JOIN dbo.plate_reader_log p
            ON p.registered_at >= d.[Date]
           AND p.registered_at < DATEADD(day, 1, d.[Date])
        GROUP BY d.[Date]
        ORDER BY d.[Date];
        """;

            await using var connection =
                new SqlConnection(_connectionString);

            await connection.OpenAsync(cancellationToken);

            var command = new CommandDefinition(
                sql,
                commandTimeout: 15,
                cancellationToken: cancellationToken);

            var result =
                await connection.QueryAsync<DailyRegistrationCount>(command);

            return result.ToList();
