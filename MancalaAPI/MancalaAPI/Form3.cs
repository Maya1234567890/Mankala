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

            pictureBox2.Parent = pictureBox1;
            pictureBox2.BackColor = Color.Transparent;

        }

        private void button1_Click(object sender, EventArgs e)
        {
            Board openForm = new Board();
            openForm.Show();
            Visible = false;
            string name = textBox1.Text, id = textBox2.Text;
            string msg = String.Format("[\'start\', \'{0}\', \'{1}\']'", name,id);
            Program.s.Send(Encoding.ASCII.GetBytes(msg));

        }
    }
}
