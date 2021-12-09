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
    public partial class StartGame : Form
    {
        public StartGame()
        {
          // upon showing the form's graphics

            InitializeComponent();

            // setting the background color
            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;
            label2.Parent = pictureBox1;
            label2.BackColor = Color.Transparent;
            pictureBox2.Parent = pictureBox1;
            pictureBox2.BackColor = Color.Transparent;

        }

        private void button1_Click(object sender, EventArgs e)
        {
          // upon clicking StartGame

            string name = textBox1.Text;
            string msg = String.Format("[\'start\', \'{0}\']", name);
            Program.s.Send(Encoding.ASCII.GetBytes(msg)); // sending the python server the user's name
            // if there is an error in the name, lets the user know and doesn't continue to the board game
            string ans = Program.ReceiveMessage();
            if (ans != "OK")  // if the server has a problem
            {
                label2.Text = ans;  // show the problem
                return;
            }

            // continue to the game
            Board openForm = new Board();
            openForm.Show();
            Visible = false;

        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {

        }
    }
}
