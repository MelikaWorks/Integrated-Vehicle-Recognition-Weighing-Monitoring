// Selected historical excerpt; imports, surrounding class and other logic omitted.
// Documentation sample only: not a complete buildable application.

            var username = _configuration["DashboardAuth:Username"];
            var passwordHash = _configuration["DashboardAuth:PasswordHash"];

            if (string.IsNullOrWhiteSpace(username) ||
                string.IsNullOrWhiteSpace(passwordHash))
            {
                ModelState.AddModelError(
                    string.Empty,
                    "تنظیمات حساب ورود تکمیل نشده است.");

                return View(model);
            }

            var hasher = new PasswordHasher<string>();

            var result = hasher.VerifyHashedPassword(
                "dashboard",
                passwordHash,
                model.Password);

            var usernameMatches = string.Equals(
                model.Username.Trim(),
                username,
                StringComparison.OrdinalIgnoreCase);

            if (!usernameMatches ||
                result == PasswordVerificationResult.Failed)
            {
                ModelState.AddModelError(
                    string.Empty,
                    "نام کاربری یا رمز عبور نادرست است.");

                model.Password = string.Empty;
                ModelState.Remove(nameof(LoginViewModel.Password));

                return View(model);
