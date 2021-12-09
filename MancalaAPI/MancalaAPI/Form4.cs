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
using System.Threading; // for a timeout

namespace MancalaAPI
{
    public partial class Board : Form
    {
        public Board()
        {
            // the function is ran upon opening the board
            InitializeComponent();

            // set the label's backgrounds
            label2.Parent = pictureBox1;
            label2.BackColor = Color.Transparent;
            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;
            Point pt = this.PointToScreen(label1.Location);
            label1.Location = pictureBox1.PointToClient(pt);

            // make a list of all the slots
            Label[] holes = { hole_0, hole_1, hole_2, hole_3, hole_4, hole_5, hole_6, hole_7,
            hole_8, hole_9, hole_10, hole_11, hole_12, hole_13};

            // setting the pit's background colors
            for (int i = 0; i < holes.Length; i++)
            {
                pt = this.PointToScreen(holes[i].Location);
                holes[i].Location = pictureBox2.PointToClient(pt);
                holes[i].Parent = pictureBox2;
                holes[i].BackColor = Color.Transparent;
            }

            // the GUI client is ready. Sending the python server a request for the game ID
            Program.s.Send(Encoding.ASCII.GetBytes("The client Entered. Sending game ID..."));
            string gameID = Program.ReceiveMessage();
            label2.Text = gameID; // setting the game ID

        }


        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
          // The function updates the board's positions and the marbels in each slot.
          // After each right key press the client updates with the latest information about the board.
          // In order to run the graphics in the best way, you'd have to constantly press the right key.
          // (Not the greatest solution at all...)

            Label[] holes = { hole_0, hole_1, hole_2, hole_3, hole_4, hole_5, hole_6, hole_7,
            hole_8, hole_9, hole_10, hole_11, hole_12, hole_13};  // make a list of all the slots

            //capture right arrow key
            if (keyData == Keys.Right)
            {
              // the client recievs a game update
                string data = Program.ReceiveMessage();

                if (!data.StartsWith("You"))  // if it's a board update
                {
                  // update the holes
                    for (int i = 0; i < holes.Length - 1; i++)
                    {
                        holes[i].Text = data.Substring(0, Program.data.IndexOf(" "));
                        data = data.Remove(0, Program.data.IndexOf(" ") + 1);
                    }

                    hole_13.Text = data;
                }
                else  // if it's the end of the game
                {
                    label1.Text = data; // update if the player won/lost
                    Thread.Sleep(1000); // let the text run for a while
                }

            }

            return true;
        }
    }
}
