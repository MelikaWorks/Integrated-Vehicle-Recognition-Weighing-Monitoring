// Selected historical excerpt; imports, surrounding class and other logic omitted.
// Documentation sample only: not a complete buildable application.

            const string sql = """
    SELECT TOP (50)
        towzin_code AS TowzinCode,
        car_pelak   AS CarPelak,
        towzin_date AS TowzinDate,
        towzin_time AS TowzinTime
    FROM dbo.towzin_tb
    WHERE
        @Search IS NULL
        OR CHARINDEX(
            @Search,
            CONVERT(nvarchar(20), towzin_code)
        ) > 0
        OR CHARINDEX(@Search, car_pelak) > 0
    ORDER BY towzin_code DESC;
    """;

            await using var connection =
                new SqlConnection(_connectionString);

            await connection.OpenAsync(cancellationToken);

