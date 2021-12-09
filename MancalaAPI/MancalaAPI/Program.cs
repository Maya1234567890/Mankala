using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text;
using System.Net.Sockets; // socket connection to the python server

namespace MancalaAPI
{
    internal static class Program
    {
        public static Socket s; // a global variable for the python socket

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainMenu());
            s.Send(Encoding.ASCII.GetBytes("['stop']"));  // signeling the python server the GUI stopped
            Environment.Exit(1);  // exit everything
        }

        public static string ReceiveMessage()
        {
          // a global function for receiving messages from the python server
          // returns the data which got sent

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
