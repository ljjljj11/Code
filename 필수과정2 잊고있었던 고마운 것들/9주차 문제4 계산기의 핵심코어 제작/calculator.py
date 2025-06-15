import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        """초기화 메서드: UI 초기화 및 계산기 상태 리셋"""
        super().__init__()
        self.init_ui()  # UI 초기화
        self.reset()  # 계산기 초기화

    def init_ui(self):
        """UI 구성: 창, 버튼, 디스플레이 구성"""
        self.setWindowTitle('Calculator')  # 창 제목 설정
        self.setGeometry(100, 100, 300, 400)  # 창 크기 설정

        # 메인 레이아웃 설정
        layout = QVBoxLayout()

        # 디스플레이 화면 설정 (결과 출력)
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)  # 화면에 숫자 오른쪽 정렬
        self.display.setReadOnly(True)  # 사용자가 텍스트를 수정하지 못하도록 설정
        self.display.setStyleSheet('font-size: 24px; padding: 10px;')  # 화면 글씨 크기와 여백 설정
        layout.addWidget(self.display)  # 디스플레이 레이아웃에 추가

        # 버튼 레이아웃 (격자형)
        buttons_layout = QGridLayout()
        buttons = [
            ('AC', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        # 버튼 생성 및 레이아웃에 추가
        for text, row, col, *span in buttons:
            button = QPushButton(text)
            button.setStyleSheet('font-size: 18px; padding: 15px;')  # 버튼 스타일 설정
            button.clicked.connect(self.on_button_click)  # 버튼 클릭 시 이벤트 처리
            if span:
                buttons_layout.addWidget(button, row, col, *span)  # 버튼 크기 조정
            else:
                buttons_layout.addWidget(button, row, col)  # 일반 버튼 추가

        layout.addLayout(buttons_layout)  # 버튼 레이아웃 추가
        self.setLayout(layout)  # 최종 레이아웃 설정

    def reset(self):
        """계산기 초기화: 기존 수식 및 화면을 초기화"""
        self.expression = ''  # 수식 초기화
        self.display.setText('0')  # 화면에 0 표시

    def add(self, a, b):
        """덧셈"""
        return a + b

    def subtract(self, a, b):
        """뺄셈"""
        return a - b

    def multiply(self, a, b):
        """곱셈"""
        return a * b

    def divide(self, a, b):
        """나눗셈 (0으로 나누면 예외 처리)"""
        if b == 0:
            raise ZeroDivisionError  # 0으로 나누기 예외 처리
        return a / b

    def negative_positive(self):
        """숫자의 부호를 반전시킴 (양/음)"""
        if self.expression:
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]  # 음수를 양수로 변경
            else:
                self.expression = '-' + self.expression  # 양수를 음수로 변경
            self.display.setText(self.expression)

    def percent(self):
        """퍼센트 계산"""
        try:
            value = float(self.expression)  # 숫자로 변환
            value /= 100  # 백분율 계산
            self.expression = str(value)
            self.display.setText(self.expression)
        except Exception:
            self.display.setText('Error')  # 오류 발생 시 에러 메시지 출력

    def add_decimal(self):
        """소수점 추가 (이미 있는 경우 중복 추가 방지)"""
        if '.' not in self.expression.split()[-1]:  # 현재 숫자에 소수점이 없다면
            self.expression += '.'  # 소수점 추가
            self.display.setText(self.expression)

    def equal(self):
        """수식을 계산하고 결과를 출력"""
        try:
            # 수식의 연산자 변경: ÷, ×를 /, *로 변환
            expr = self.expression.replace('×', '*').replace('÷', '/')

            # 수식 계산
            result = eval(expr)

            # 결과가 너무 큰 경우 Overflow 처리
            if abs(result) > 1e308:
                raise OverflowError

            # 결과를 화면에 출력
            self.expression = str(result)
            self.display.setText(self.expression)

        except ZeroDivisionError:
            self.display.setText('Cannot divide by zero')  # 0으로 나누기 오류
            self.expression = ''  # 수식 초기화
        except OverflowError:
            self.display.setText('Number out of range')  # 범위 초과 오류
            self.expression = ''  # 수식 초기화
        except Exception:
            self.display.setText('Error')  # 기타 오류 처리
            self.expression = ''  # 수식 초기화

    def on_button_click(self):
        """버튼 클릭 시 이벤트 처리"""
        text = self.sender().text()  # 클릭된 버튼의 텍스트를 가져옴

        # 버튼에 따라 처리
        if text == 'AC':  # 'AC' 버튼을 누르면 계산기 초기화
            self.reset()
        elif text == '+/-':  # '+/-' 버튼을 누르면 부호 변경
            self.negative_positive()
        elif text == '%':  # '%' 버튼을 누르면 퍼센트 계산
            self.percent()
        elif text == '=':  # '=' 버튼을 누르면 수식 계산
            self.equal()
        elif text == '.':  # '.' 버튼을 누르면 소수점 추가
            self.add_decimal()
        elif text in '0123456789':  # 숫자 버튼을 누르면 수식에 숫자 추가
            self.expression += text
            self.display.setText(self.expression)
        elif text in '+-×÷':  # 연산자 버튼을 누르면 수식에 연산자 추가
            if self.expression and self.expression[-1] not in '+-×÷':  # 연속된 연산자 방지
                self.expression += text
                self.display.setText(self.expression)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt5 애플리케이션 시작
    calc = Calculator()  # 계산기 인스턴스 생성
    calc.show()  # 계산기 화면 표시
    sys.exit(app.exec_())  # 애플리케이션 실행 종료
