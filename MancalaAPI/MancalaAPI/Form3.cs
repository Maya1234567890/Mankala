using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.Net.Sockets;

namespace MancalaAPI
{
    public partial class JoinGame : Form
    {
        public JoinGame()
        {
            InitializeComponent();

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
            
            string name = textBox2.Text, id = textBox1.Text;
            string msg = String.Format("[\'join\', \'{0}\', \'{1}\']", name,id);
            Program.s.Send(Encoding.ASCII.GetBytes(msg));

            string ans = Program.ReceiveMessage();
            if (ans != "OK")
            {
                label3.Text = ans;
                return;
            }

            Board openForm = new Board();
            openForm.Show();
            Visible = false;

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }
    }
}
