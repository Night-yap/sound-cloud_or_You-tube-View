import sys
import psutil
import pygetwindow as gw
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush

# 実行中のメディアプレーヤーを探し、そのタイトルを取得
def get_media_info():
        # ChromeやEdgeでSoundCloudを開いている場合
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe' or proc.info['name'] == 'msedge.exe' or proc.info['name'] == 'brave.exe':
            windows = gw.getWindowsWithTitle('Youtube')
            if windows:
                return windows[0].title
    return "nothing"

# メディア制御関数（再生、停止、次の曲）
def control_media(action):
    if action == "play_pause":
        pyautogui.press('playpause')  # playpauseで再生/停止
    elif action == "next":
        pyautogui.press('nexttrack')  # 次の曲
    elif action == "previous":
        pyautogui.press('prevtrack')  # 前の曲

class SettingsWindow(QWidget):
    def __init__(self, overlay):
        super().__init__()

        self.overlay = overlay
        self.setWindowTitle("設定")
        self.setGeometry(200, 300, 300, 180)
        
        # 現在の背景色と文字色を取得
        bg_value = self.overlay.background_color.red()  # 背景色の赤成分
        text_value = self.overlay.text_color.red()  # 文字色の赤成分
        bg_color_value = self.overlay.background_color.alpha()  # 背景色の不透明度
        tx_speed_value = self.overlay.scroll_speed  # スクロール速度
        tx_sleep_value = self.overlay.pause_duration_N  # 変更なし���り再生時間

        # 背景色を変更するスライダー（0が黒、255が白）
        self.bg_slider = QSlider(Qt.Horizontal, self)
        self.bg_slider.setMinimum(0)
        self.bg_slider.setMaximum(255)
        self.bg_slider.setValue(bg_value)  # 現在の背景色に設定
        self.bg_slider.valueChanged.connect(self.change_bg_color)

        # 文字色を変更するスライダー（0が黒、255が白）
        self.text_slider = QSlider(Qt.Horizontal, self)
        self.text_slider.setMinimum(0)
        self.text_slider.setMaximum(255)
        self.text_slider.setValue(text_value)  # 現在の文字色に設定
        self.text_slider.valueChanged.connect(self.change_text_color)

        # 透明度を変更するスライダー（0が完全透明、255が不透明）
        self.opacity_slider = QSlider(Qt.Horizontal, self)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(255)
        self.opacity_slider.setValue(bg_color_value)  # 初期値
        self.opacity_slider.valueChanged.connect(self.change_opacity)

        #テキストスピード
        self.scroll_speed_slider = QSlider(Qt.Horizontal, self)
        self.scroll_speed_slider.setMinimum(1)
        self.scroll_speed_slider.setMaximum(5)
        self.scroll_speed_slider.setValue(tx_speed_value)  # 初期値
        self.scroll_speed_slider.valueChanged.connect(self.change_scroll_speed)

        #テキストスリープ
        self.pause_duration_slinder = QSlider(Qt.Horizontal, self)
        self.pause_duration_slinder.setMinimum(0)
        self.pause_duration_slinder.setMaximum(10)
        self.pause_duration_slinder.setValue(tx_sleep_value)  # 初期値
        self.pause_duration_slinder.valueChanged.connect(self.change_pause_duration_timer)



        # レイアウトを作成
        layout = QVBoxLayout()
        layout.addWidget(QLabel("背景色:"))
        layout.addWidget(self.bg_slider)
        layout.addWidget(QLabel("文字色:"))
        layout.addWidget(self.text_slider)
        layout.addWidget(QLabel("透明度:"))
        layout.addWidget(self.opacity_slider)
        layout.addWidget(QLabel("scroll_speed:"))
        layout.addWidget(self.scroll_speed_slider)
        layout.addWidget(QLabel("pause_duration_timer:"))
        layout.addWidget(self.pause_duration_slinder)
        self.setLayout(layout)

    def change_bg_color(self, value):
        self.overlay.update_background_color(value)

    def change_text_color(self, value):
        self.overlay.update_text_color(value)

    def change_opacity(self, value):
        self.overlay.update_opacity(value)

    def change_scroll_speed(self, value):
        self.overlay.update_scroll_speed(value)

    def change_pause_duration_timer(self, value):
        self.overlay.update_pause_duration_timer(value)


class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 500, 100)
        
        # 初期の背景色（黒に透明度160）と文字色（白）
        self.background_color = QColor(0, 0, 0, 160)
        self.text_color = QColor(255, 255, 255)  # 白色

        #透明初期
        self.background_color.setAlpha(160)  

        #テキストスピードのやつ
        self.scroll_speed = 1
        self.pause_duration = 3000

        # ラベルを作成してメディア情報を表示
        self.label = QLabel(self)
        self.label.setFont(QFont("Arial", 12))
        self.label.setStyleSheet(f"color: {self.text_color.name()};")
        self.label.setText("-You_tube_View-")
        self.label.move(10, 10)

        # スクロールさせるテキスト
        self.scroll_label = QLabel(self)
        self.scroll_label.setFont(QFont("Arial", 10))
        self.scroll_label.setStyleSheet(f"color: {self.text_color.name()};")
        self.scroll_label.setText(":-----------------------------------------------------------------------------------------------------------\
-----------------------------------------------------------------------------------------------------------------------------------------------\
-------------------------------------------------------")
        self.scroll_label.move(10, 40)  # 初期位置

        # 再生・停止ボタン
        self.play_pause_btn = QPushButton("Play/Pause", self)
        self.play_pause_btn.move(10, 70)
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)

        # 次の曲ボタン
        self.next_btn = QPushButton("Next", self)
        self.next_btn.move(190, 70)
        self.next_btn.clicked.connect(self.skip_next)

        # 前の曲ボタン
        self.previous_btn = QPushButton("Previous", self)
        self.previous_btn.move(100, 70)
        self.previous_btn.clicked.connect(self.previous)

        # 設定ボタン
        self.settings_btn = QPushButton("設定", self)
        self.settings_btn.move(280, 70)
        self.settings_btn.clicked.connect(self.open_settings_window)

        #Exit
        self.Exit_btn = QPushButton("Exit", self)
        self.Exit_btn.move(370, 70)
        self.Exit_btn.clicked.connect(self.Exit_button)

        # 初期位置
        self.oldPos = self.pos()

        # テキストのスクロール設定
        self.text_x_pos = 10  # 初期のテキストのx座標
        self.scroll_speed = 1  # テキストが動く速度
        self.window_width = self.width()

        # テキストがスクロールするかどうかの初期設定
        self.should_scroll = False  # 初期状態ではスクロールしない
        self.is_paused = False  # スクロール停止のフラグ
        self.pause_duration_N = 3  # 停止時間（ミリ秒）--------------------------------------------------------------TIME
        self.pause_timer = QTimer(self)  # タイマーの設定
        self.pause_timer.setSingleShot(True)  # 一度だけ動作
        self.pause_timer.timeout.connect(self.resume_scroll)  # 停止後に再開

        # タイマー設定
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.scroll_text)
        self.scroll_timer.start(30)  # 30msごとにテキストを動かす
        

    def update_media_info(self, media_info):
        # 新しいテキストに更新
        print(f"SoundCloud再生中?: {media_info}")
        self.scroll_label.setText(f":{media_info}")
        # 文字列の幅を再計算
        self.text_length = self.scroll_label.fontMetrics().width(self.scroll_label.text())
        # スクロールするかどうかの条件を再評価
        self.should_scroll = self.text_length > self.window_width - 20
        # 初期位置にリセット<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<こいつが悪い
        #self.text_x_pos = 10

    def toggle_play_pause(self):
        control_media("play_pause")

    def skip_next(self):
        control_media("next")
    def previous(self):
        control_media("previous")

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def Exit_button(self):
        sys.exit()

    def update_background_color(self, value):
        # スライダーの値に応じて背景色を黒から白に変更
        self.background_color.setRed(value)
        self.background_color.setGreen(value)
        self.background_color.setBlue(value)
        self.update()

    def update_text_color(self, value):
        # スライダーの値に応じて文字色を黒から白に変更
        self.text_color.setRed(value)
        self.text_color.setGreen(value)
        self.text_color.setBlue(value)
        self.label.setStyleSheet(f"color: {self.text_color.name()};")
        self.scroll_label.setStyleSheet(f"color: {self.text_color.name()};")

    def update_opacity(self, value):
        print(f"スライダーの値: {value}") # ここでスライダーの値を確認
        # スライダーの値に応じて背景の透明度を変更
        self.background_color.setAlpha(value)   
        self.update()

    def update_scroll_speed(self,value):
        self.scroll_speed = value  # スライダーのテキストスピード値をアップデート
        

    def update_pause_duration_timer(self, value):
        self.pause_duration_N = value  # 待ち時間の値をアップデート
        self.pause_duration = self.pause_duration_N*1000 #1000倍に

    def scroll_text(self):
        # テキストがウィンドウより長い場合のみスクロール
        if self.should_scroll and not self.is_paused:
            self.text_x_pos -= self.scroll_speed# スクロールするスピードを更新
            #print(f"テキストのxスピード: {self.scroll_speed}")
            if self.text_x_pos + self.text_length < 0:  # テキストがウィンドウの左端を超えたら＿＿機能してない！！！__なんとかなった
                #self.text_x_pos = self.window_width  # 右端に戻さない
                self.text_x_pos = 10 #もとに戻す
                # スクロールを2秒間停止
                self.is_paused = True
                self.pause_timer.start(self.pause_duration)  # 2秒後に再開

            # テキストの新しい位置にラベルを配置_X座標を更新してる
            self.scroll_label.move(self.text_x_pos, 40)
            #ここで時間停止？
            
        else:
            # テキストが短い場合は初期位置に戻す
            self.scroll_label.move(10, 40)
    def resume_scroll(self):
        # 2秒後にスクロールを再開
        self.is_paused = False

    def mousePressEvent(self, event):
        # マウスが押された位置を記録
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        # マウスが動いたときの位置からウィンドウの位置を更新
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def paintEvent(self, event):
        # 背景を描画してぼかし効果をつける
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # スライダーの値で変更された背景色を使用
        brush = QBrush(self.background_color)  
        painter.setBrush(brush)
        painter.drawRoundedRect(self.rect(), 10, 10)  # 角を丸めた背景


def main():
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    overlay.show()

    def update_overlay():
        media_info = get_media_info()
        print(f"SoundCloud再生中: {media_info}")
        overlay.update_media_info(media_info)

    timer = QTimer()
    timer.timeout.connect(update_overlay)
    timer.start(500)  # 0.5秒ごとにメディア情報を更新

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
