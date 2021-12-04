using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using IronPython.Hosting;

namespace MancalaAPI
{
    public partial class Board : Form
    {
        public Board()
        {
            InitializeComponent();

            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;

            label2.Parent = pictureBox1;
            label2.BackColor = Color.Transparent;

            label3.Parent = pictureBox1;
            label3.BackColor = Color.Transparent;

            Label[] holes = { hole_0, hole_1, hole_2, hole_3, hole_4, hole_5, hole_6, hole_7,
            hole_8, hole_9, hole_10, hole_11, hole_12, hole_13};

            for (int i = 0; i < holes.Length; i++)
            {
                Point pt = this.PointToScreen(holes[i].Location);
                holes[i].Location = pictureBox2.PointToClient(pt);
                holes[i].Parent = pictureBox2;
                holes[i].BackColor = Color.Transparent;
            }

            var py = Python.CreateEngine();
            try
            {
                py.ExecuteFile("script.py");
            }
            catch (Exception ex)
            {
                Console.WriteLine(
                   "Oops! We couldn't execute the script because of an exception: " + ex.Message);
            }
        }

    }
}
