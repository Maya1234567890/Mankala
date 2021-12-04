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
    public partial class MainMenu : Form
    {
        public MainMenu()
        {
            InitializeComponent();

            label1.Parent = pictureBox1;
            label1.BackColor = Color.Transparent;

            label2.Parent = pictureBox1;
            label2.BackColor = Color.Transparent;

            var py = Python.CreateEngine();
            var scope = py.CreateScope();
            var libs = new[] {
    "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\Common7\\IDE\\Extensions\\Microsoft\\Python Tools for Visual Studio\\2.2",
    "C:\\Program Files\\IronPython 3.4\\Lib",
    "C:\\Program Files\\IronPython 3.4\\DLLs",
    "C:\\Program Files (x86)\\IronPython 3.4",
    "C:\\Program Files (x86)\\IronPython 3.4\\lib\\site-packages"
};

            py.SetSearchPaths(libs);

            try
            {
                py.ExecuteFile("script.py", scope);
            }
            catch (Exception ex)
            {
                Console.WriteLine(
                   "Oops! We couldn't execute the script because of an exception: " + ex.Message);
            }
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
