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
using System.Threading;

namespace MancalaAPI
{
    public partial class Board : Form
    {
        public Board()
        {
            InitializeComponent();

            label2.Parent = pictureBox1;
            label2.BackColor = Color.Transparent;
            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;
            Point pt = this.PointToScreen(label1.Location);
            label1.Location = pictureBox1.PointToClient(pt);

            Label[] holes = { hole_0, hole_1, hole_2, hole_3, hole_4, hole_5, hole_6, hole_7,
            hole_8, hole_9, hole_10, hole_11, hole_12, hole_13};

            for (int i = 0; i < holes.Length; i++)
            {
                pt = this.PointToScreen(holes[i].Location);
                holes[i].Location = pictureBox2.PointToClient(pt);
                holes[i].Parent = pictureBox2;
                holes[i].BackColor = Color.Transparent;
            }
            Program.s.Send(Encoding.ASCII.GetBytes("The client Entered. Sending game ID..."));
            string gameID = Program.ReceiveMessage();
            label2.Text = gameID;

        }


        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            Label[] holes = { hole_0, hole_1, hole_2, hole_3, hole_4, hole_5, hole_6, hole_7,
            hole_8, hole_9, hole_10, hole_11, hole_12, hole_13};

            //capture right arrow key
            if (keyData == Keys.Right)
            {
                string data = Program.ReceiveMessage();

                if (!data.StartsWith("You"))
                {
                    for (int i = 0; i < holes.Length - 1; i++)
                    {
                        holes[i].Text = data.Substring(0, Program.data.IndexOf(" "));
                        data = data.Remove(0, Program.data.IndexOf(" ") + 1);
                    }

                    hole_13.Text = data;
                }
                else
                {
                    label1.Text = data;
                    Thread.Sleep(1000);
                }

            }

            return true;
        }
    }
}
