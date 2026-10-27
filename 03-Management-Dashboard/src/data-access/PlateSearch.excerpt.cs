// Selected historical excerpt; imports, surrounding class and other logic omitted.
// Documentation sample only: not a complete buildable application.


            const string sql = """
        SELECT TOP (50)
            id                  AS Id,
            towzin_code         AS TowzinCode,
            car_pelak           AS CarPelak,
            registered_at       AS RegisteredAt,
            registration_source AS RegistrationSource,
            plate_image_name    AS PlateImageName,
            plate_image_path    AS PlateImagePath,
            vehicle_image_name  AS VehicleImageName,
            vehicle_image_path  AS VehicleImagePath
        FROM dbo.plate_reader_log
        WHERE @Search IS NULL
           OR CHARINDEX(@Search, towzin_code) > 0
           OR CHARINDEX(@Search, car_pelak) > 0
        ORDER BY registered_at DESC, id DESC;
        """;

            await using var connection =
                new SqlConnection(_connectionString);

            await connection.OpenAsync(cancellationToken);

            var command = new CommandDefinition(
                sql,
