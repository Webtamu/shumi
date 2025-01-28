using System.Windows;
using System;
using System.Diagnostics;
using System.Threading;
namespace Jam_App_Project
{
    public partial class MainWindow : Window
    {
        bool running;
        Stopwatch stopWatch = new Stopwatch();
        public MainWindow()
        {
            InitializeComponent();
            running = false;

        }

        private void btnToggle_Click(object sender, RoutedEventArgs e)
        {
            
            if (!running)
            {
                stopWatch.Start();
                txtStatus.Text = "Running!";
                btnToggle.Content = "Pause Session";
            }
            else
            {
                stopWatch.Stop();
                txtStatus.Text = stopWatch.Elapsed.ToString();
                btnToggle.Content = "Continue Session";
            }
            running = !running;
        }
    }
}
