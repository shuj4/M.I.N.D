import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from scipy.fft import fft, fftfreq
from chords_serial import Chords_USB
import threading
import cursor_control as cursor_control  # Adjust path if needed


class EEGWindow(QtWidgets.QWidget):
    def __init__(self, device):
        super().__init__()

        self.device = device
        self.num_channels = self.device.num_channels
        self.data = self.device.data
        self.curves = []

        self.sampling_rate = self.device.supported_boards[self.device.board]["sampling_rate"]
        self.brainwave_heights = [0, 0, 0, 0, 0]  # Delta, Theta, Alpha, Beta, Gamma

        self.initUI()

        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.update_plots)
        self.plot_timer.start(10)

        self.fft_timer = QtCore.QTimer()
        self.fft_timer.timeout.connect(self.update_brainwaves)
        self.fft_timer.start(1000)

        # Start Tkinter GUI in separate thread
        threading.Thread(target=cursor_control.start_cursor_gui, daemon=True).start()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # EEG line plots
        for i in range(self.num_channels):
            plot = pg.PlotWidget(title=f"Channel {i+1}")
            plot.setYRange(0, 2500)
            plot.showGrid(x=True, y=True)
            curve = plot.plot(pen=pg.mkPen(color=pg.intColor(i, hues=6), width=2))
            self.curves.append(curve)
            layout.addWidget(plot)

        # Bar graph for brainwaves
        self.brainwave_plot = pg.PlotWidget(title="Brainwave Power")
        self.brainwave_plot.setMinimumHeight(500)
        self.brainwave_plot.setMaximumHeight(600)
        self.brainwave_plot.setYRange(0, 50000)
        self.brainwave_plot.setLabel('left', 'Power')
        self.brainwave_plot.setLabel('bottom', 'Waves')
        self.brainwave_plot.showGrid(x=True, y=True)

        self.brainwave_x = [1, 2, 3, 4, 5]
        self.brainwave_labels = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
        self.brainwave_colors = ['#00aaff', '#55dd33', '#ffaa00', '#ff4444', '#aa00ff']

        self.bar_items = pg.BarGraphItem(
            x=self.brainwave_x,
            height=self.brainwave_heights,
            width=0.8,
            brushes=self.brainwave_colors
        )
        self.brainwave_plot.addItem(self.bar_items)
        self.brainwave_plot.getAxis('bottom').setTicks([list(zip(self.brainwave_x, self.brainwave_labels))])
        layout.addWidget(self.brainwave_plot)

        self.setWindowTitle("EEG Real-time Analyzer")
        self.setLayout(layout)
        self.show()

    def update_plots(self):
        self.device.read_data()
        for i in range(self.num_channels):
            self.curves[i].setData(self.device.data[i])

    def update_brainwaves(self):
        eeg_signal = np.array(self.device.data[0])
        if len(eeg_signal) < 256:
            return

        fft_result = np.abs(fft(eeg_signal))
        freqs = fftfreq(len(eeg_signal), d=1/self.sampling_rate)
        freqs = freqs[:len(freqs)//2]
        fft_result = fft_result[:len(freqs)]

        bands = {
            'Delta': (0.5, 4),
            'Theta': (4, 10),
            'Alpha': (10, 15),
            'Beta': (15, 35),
            'Gamma': (35, 50)
        }

        new_powers = []
        for band in bands.values():
            power = np.sum(fft_result[(freqs >= band[0]) & (freqs < band[1])])
            new_powers.append(power)

        alpha = 0.2
        self.brainwave_heights = [
            alpha * new + (1 - alpha) * old
            for new, old in zip(new_powers, self.brainwave_heights)
        ]

        self.bar_items.setOpts(height=self.brainwave_heights)

        beta_power = self.brainwave_heights[3]
        gamma_power = self.brainwave_heights[4]

        print(f"📊 Gamma: {gamma_power:.2f}, Beta: {beta_power:.2f}")  # Debug

        if gamma_power > 25000:
            print("⬆️ Cursor Move Triggered: UP (Gamma wave threshold crossed)")
            cursor_control.move_cursor("UP")

        if beta_power > 15000:
            print("⬇️ Cursor Move Triggered: DOWN (Beta wave threshold crossed)")
            cursor_control.move_cursor("DOWN")


def main():
    app = QtWidgets.QApplication(sys.argv)

    device = Chords_USB()
    if not device.detect_hardware():
        print("❌ No supported hardware found.")
        sys.exit(1)

    device.send_command("START")
    win = EEGWindow(device)

    ret = app.exec_()
    device.cleanup()
    sys.exit(ret)


if __name__ == "__main__":
    main()

