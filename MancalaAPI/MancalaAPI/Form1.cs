﻿using System;
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
    
    public partial class MainMenu : Form
    {
        //public static Socket s;
        public MainMenu()
        {
            InitializeComponent();

            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;

            label2.Parent = pictureBox1;
            label2.BackColor = Color.Transparent;

            Program.s = new Socket(AddressFamily.InterNetwork,
                SocketType.Stream, ProtocolType.Tcp);
            Program.s.Connect("localhost", 45000);

        }

        private void button1_Click(object sender, EventArgs e)
        {
            StartGame openForm = new StartGame();
            openForm.Show();
            Visible = false;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            JoinGame openForm = new JoinGame();
            openForm.Show();
            Visible = false;
        }
    }
}
