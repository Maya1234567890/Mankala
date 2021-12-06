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

            Label[] holes = { hole_0, hole_1, hole_2, hole_3, hole_4, hole_5, hole_6, hole_7,
            hole_8, hole_9, hole_10, hole_11, hole_12, hole_13};

            for (int i = 0; i < holes.Length; i++)
            {
                Point pt = this.PointToScreen(holes[i].Location);
                holes[i].Location = pictureBox2.PointToClient(pt);
                holes[i].Parent = pictureBox2;
                holes[i].BackColor = Color.Transparent;
            }
            Program.s.Send(Encoding.ASCII.GetBytes("The client Entered. Sending game ID..."));
            string gameID = Program.ReceiveMessage();
            label2.Text = gameID;

        }

        public void BeginBoard(Label[] holes)
        {
            //Program.s.Send(Encoding.ASCII.GetBytes("The client Entered. Sending game ID..."));
            //string gameID = Program.ReceiveMessage();
            //label2.Text = gameID;

            string data = Program.ReceiveMessage();

            Console.WriteLine(data);

            if (data.StartsWith("Error")) { }
            else if (data.StartsWith("Game Over")) { }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Program.s.Send(Encoding.ASCII.GetBytes("['Board request']"));
            string data = Program.ReceiveMessage();

            Label[] holes = { hole_0, hole_1, hole_2, hole_3, hole_4, hole_5, hole_6, hole_7,
            hole_8, hole_9, hole_10, hole_11, hole_12, hole_13};

            if (data != "wait")
            {
                Console.WriteLine(data);
                Program.data = data;

                button1.Text = "Press Right";
                button1.Enabled = false;


                //while (data != "True" & data != "False")
                //{
                //    for (int i = 0; i < holes.Length; i++)
                //    {
                //        Console.WriteLine("before" + data);
                //        if (i < 13)
                //        {
                //            holes[i].Text = data.Substring(0, data.IndexOf(" "));
                //            data = data.Remove(0, data.IndexOf(" ") + 1);
                //        }
                //        else
                //        {
                //            holes[i].Text = data.Substring(0, data.IndexOf("-"));
                //            data = data.Remove(0, data.IndexOf('-'));
                //        }
                //        Thread.Sleep(10);

                //        Console.WriteLine("after" + data);
                //    }
                //    data = data.Remove(0, 2);
                //    Console.WriteLine("after after" + data);
                //}
            }
            else
            { //message box}

            }
        }

        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            Label[] holes = { hole_0, hole_1, hole_2, hole_3, hole_4, hole_5, hole_6, hole_7,
            hole_8, hole_9, hole_10, hole_11, hole_12, hole_13};

            //capture right arrow key
            if (keyData == Keys.Right)
            {
                if (Program.data is null) return true;
                if (Program.data != "True" & Program.data != "False")
                {
                    if (Program.data[0] == '-') Program.data = Program.data.Remove(0, 2);
                    if (Program.data == "True" || Program.data == "False") return true;


                    while (Program.data.IndexOf(" ") < Program.data.IndexOf("-") &
                        Program.data.IndexOf(" ") != -1)
                    {
                        holes[Program.c].Text = Program.data.Substring(0, Program.data.IndexOf(" "));
                        Program.data = Program.data.Remove(0, Program.data.IndexOf(" ") + 1);
                        Program.c++;
                    }
                    
                    
                    Console.WriteLine(Program.data);
                    hole_13.Text = Program.data.Substring(0, Program.data.IndexOf("-"));
                    Program.data = Program.data.Remove(0, Program.data.IndexOf('-'));
                    Program.c = 0;
                    
                }
                else
                {
                    Thread.Sleep(3000);
                    EndWindow form5 = new EndWindow();
                    form5.Show();
                    Visible = false;
                }
            }
            return true;
        }
    }
}
