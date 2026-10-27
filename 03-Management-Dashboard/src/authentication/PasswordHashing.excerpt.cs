// Selected historical excerpt; imports, surrounding class and other logic omitted.
// Documentation sample only: not a complete buildable application.

    var hasher =
        new Microsoft.AspNetCore.Identity.PasswordHasher<string>();

    Console.WriteLine(
        hasher.HashPassword("dashboard", password.ToString()));
