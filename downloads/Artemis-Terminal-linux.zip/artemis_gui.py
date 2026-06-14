import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QFrame
)

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Artemis(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARTEMIS")
        self.resize(1600, 900)

        # MAIN
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        central.setLayout(main_layout)

        # SIDEBAR
        sidebar = QFrame()
        sidebar.setFixedWidth(95)

        sidebar.setStyleSheet("""
            QFrame {
                background: rgba(20, 25, 40, 0.95);
                border-radius: 28px;
            }
        """)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(18)

        sidebar.setLayout(sidebar_layout)

        # LOGO
        logo = QLabel("A")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo.setStyleSheet("""
            color: white;
            font-size: 30px;
            font-weight: bold;
        """)

        sidebar_layout.addWidget(logo)

        # BUTTONS
        buttons = [
            ("🏠", "Home"),
            ("🪐", "Inspector"),
            ("🔍", "Search"),
            ("🤖", "AI"),
            ("☁", "Cloud"),
            ("⚙", "Settings")
        ]

        for icon, name in buttons:

            btn = QPushButton(icon)

            btn.setToolTip(name)

            btn.setFixedSize(62, 62)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #111827;
                    border: none;
                    border-radius: 20px;
                    color: #60A5FA;
                    font-size: 24px;
                }

                QPushButton:hover {
                    background-color: #2563EB;
                    color: white;
                }
            """)

            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # CONTENT AREA
        content = QVBoxLayout()
        content.setSpacing(20)

        # TOP BAR
        topbar = QFrame()

        topbar.setFixedHeight(85)

        topbar.setStyleSheet("""
            QFrame {
                background-color: rgba(17,24,39,0.95);
                border-radius: 24px;
            }
        """)

        topbar_layout = QHBoxLayout()
        topbar_layout.setContentsMargins(25, 10, 25, 10)

        topbar.setLayout(topbar_layout)

        # TITLES
        titles = QVBoxLayout()

        title = QLabel("ARTEMIS OS")

        title.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
        """)

        subtitle = QLabel("Advanced Cyber Workspace")

        subtitle.setStyleSheet("""
            color: #94A3B8;
            font-size: 14px;
        """)

        titles.addWidget(title)
        titles.addWidget(subtitle)

        topbar_layout.addLayout(titles)

        topbar_layout.addStretch()

        # STATUS
        status = QLabel("SYSTEM ONLINE")

        status.setStyleSheet("""
            background-color: #052e16;
            color: #4ade80;
            padding: 10px 18px;
            border-radius: 14px;
            font-size: 13px;
            font-weight: bold;
        """)

        topbar_layout.addWidget(status)

        # TERMINAL PANEL
        terminal_frame = QFrame()

        terminal_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15,23,42,0.98);
                border-radius: 28px;
            }
        """)

        terminal_layout = QVBoxLayout()
        terminal_layout.setContentsMargins(25, 25, 25, 25)

        terminal_frame.setLayout(terminal_layout)

        terminal_title = QLabel("Terminal")

        terminal_title.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)

        terminal = QTextEdit()

        terminal.setFont(QFont("Consolas", 12))

        terminal.setStyleSheet("""
            QTextEdit {
                background-color: #020617;
                color: #60A5FA;
                border: 1px solid #1E293B;
                border-radius: 18px;
                padding: 20px;
            }
        """)

        terminal.setText("""
[ ARTEMIS BOOTLOADER ]

Loading modules...
Loading plugins...
Loading AI systems...

SYSTEM READY.
""")

        terminal_layout.addWidget(terminal_title)
        terminal_layout.addSpacing(10)
        terminal_layout.addWidget(terminal)

        # ADD
        content.addWidget(topbar)
        content.addWidget(terminal_frame)

        # MAIN
        main_layout.addWidget(sidebar)
        main_layout.addLayout(content)

        # WINDOW STYLE
        self.setStyleSheet("""
            QMainWindow {
                background-color: #030712;
            }
        """)


app = QApplication(sys.argv)

window = Artemis()
window.show()

sys.exit(app.exec())