using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MancalaAPI
{
    public partial class StartGame : Form
    {
        public StartGame()
        {
            InitializeComponent();

            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;

            pictureBox2.Parent = pictureBox1;
            pictureBox2.BackColor = Color.Transparent;

        }

        private void button1_Click(object sender, EventArgs e)
        {
            Board openForm = new Board();
            openForm.Show();
            Visible = false;
        }
    }
}
