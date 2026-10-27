// Selected C# control-message helpers; P/Invoke declarations, discovery, UI and other code omitted.
// Not a complete buildable agent.
        internal static IntPtr Message(IntPtr h, uint msg, IntPtr wp, IntPtr lp)
        {
            UIntPtr result;
            if (SendTimeout(h, msg, wp, lp, 3, 1000, out result) == IntPtr.Zero)
                throw new InvalidOperationException("ارتباط با کنترل توزین انجام نشد (timeout/access). ابزار را در نشست کاربر توزین و با سطح دسترسی مناسب اجرا کنید.");
            return IntPtr.Size == 8 ? new IntPtr(unchecked((long)result.ToUInt64())) : new IntPtr(unchecked((int)result.ToUInt32()));
        }
        internal static IntPtr MessageText(IntPtr h, uint msg, IntPtr wp, string text)
        {
            IntPtr buffer = Marshal.StringToHGlobalUni(text);
            try { return Message(h, msg, wp, buffer); }
            finally { Marshal.FreeHGlobal(buffer); }
        }
