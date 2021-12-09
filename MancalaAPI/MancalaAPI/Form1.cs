using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets; // using socket connection


namespace MancalaAPI
{

    public partial class MainMenu : Form
    {
        public MainMenu()
        {
          // the function runs before the GUI is presented
            InitializeComponent();

            // setting background color
            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;
            label2.Parent = pictureBox1;
            label2.BackColor = Color.Transparent;

            // initisalize the socket connection with the python server
            Program.s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            Program.s.Connect("127.0.0.1", 45000);
        }

        private void button1_Click(object sender, EventArgs e)
        {
          // upon clicking the "start game" button
            StartGame openForm = new StartGame();
            openForm.Show();
            Visible = false;
        }

        private void button2_Click(object sender, EventArgs e)
        {
          // upon clicking the "join game" button
            JoinGame openForm = new JoinGame();
            openForm.Show();
            Visible = false;
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }
    }
}
