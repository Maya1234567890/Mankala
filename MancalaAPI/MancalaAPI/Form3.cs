using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets; // for socket connection

namespace MancalaAPI
{
    public partial class JoinGame : Form
    {
        public JoinGame()
        {
          // upon showing the form's graphics

            InitializeComponent();

            // setting the background color
            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;
            label2.Parent = pictureBox1;
            label2.BackColor = Color.Transparent;
            label3.Parent = pictureBox1;
            label3.BackColor = Color.Transparent;
            pictureBox2.Parent = pictureBox1;
            pictureBox2.BackColor = Color.Transparent;

        }

        private void button1_Click(object sender, EventArgs e)
        {
          // upom clicing JoinGame

            string name = textBox2.Text, id = textBox1.Text;
            string msg = String.Format("[\'join\', \'{0}\', \'{1}\']", name,id);
            Program.s.Send(Encoding.ASCII.GetBytes(msg)); // sending the python server the user's name and game ID
            // if there is an error in the name, lets the user know and doesn't continue to the board game
            string ans = Program.ReceiveMessage();
            if (ans != "OK")  // if the server has a problem
            {
                label3.Text = ans; // show the problem
                return;
            }

            // continue to the game
            Board openForm = new Board();
            openForm.Show();
            Visible = false;

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }
    }
}
