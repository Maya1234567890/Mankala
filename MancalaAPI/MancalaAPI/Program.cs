using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text;
using System.Net.Sockets;

namespace MancalaAPI
{
    internal static class Program
    {
        public static Socket s;
        public static string data;
        public static int c = 0;
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainMenu());
            s.Send(Encoding.ASCII.GetBytes("['stop']"));
            Environment.Exit(1);
        }

        public static string ReceiveMessage()
        {
            byte[] bytes = new byte[3000];
            int byteCount = 0;
            // chatch exception
            try
            {
                byteCount = s.Receive(bytes, 0, bytes.Length, SocketFlags.None);
            }
            catch (SocketException)
            {
                Console.WriteLine("The python server exited");
                Environment.Exit(1);
            }
            string data = "";
            if (byteCount > 0)
            {
                data = Encoding.UTF8.GetString(bytes, 0, byteCount);
            }
            return data;
        }
    }
}
