#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
橡胶接头报价工具主程序
集成产品管理和报价计算功能
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                            QWidget, QVBoxLayout, QMessageBox, QDesktopWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from models import ProductDataModel, QuotationModel
from product_manager import ProductManagerWidget
from quotation_calculator import QuotationCalculatorWidget


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        
        # 初始化数据模型
        self.product_model = ProductDataModel()
        self.quotation_model = QuotationModel(self.product_model)
        
        # 设置窗口属性
        self.setWindowTitle("橡胶接头报价工具")
        self.setGeometry(100, 100, 1000, 700)
        self.center_window()
        
        # 确保数据目录存在
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # 初始化界面
        self.init_ui()
    
    def init_ui(self):
        """初始化UI界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 创建产品管理标签页
        product_manager = ProductManagerWidget(self.product_model)
        tab_widget.addTab(product_manager, "产品管理")
        
        # 创建报价计算标签页
        quotation_calculator = QuotationCalculatorWidget(self.product_model, self.quotation_model)
        tab_widget.addTab(quotation_calculator, "报价计算")
        
        # 标签页切换事件
        tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # 将标签页添加到主布局
        main_layout.addWidget(tab_widget)
        
        # 保存引用以便后续更新
        self.tab_widget = tab_widget
        self.product_manager = product_manager
        self.quotation_calculator = quotation_calculator
    
    def on_tab_changed(self, index):
        """
        标签页切换事件处理函数
        
        Args:
            index (int): 新的标签页索引
        """
        # 当从产品管理切换到报价计算时更新下拉框
        if index == 1:  # 报价计算标签页
            self.quotation_calculator.update_type_combos()
    
    def center_window(self):
        """将窗口居中显示"""
        # 获取屏幕几何信息
        screen_geometry = QDesktopWidget().availableGeometry()
        window_geometry = self.frameGeometry()
        
        # 计算居中位置
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        
        # 移动窗口
        self.move(window_geometry.topLeft())
    
    def closeEvent(self, event):
        """
        窗口关闭事件处理
        
        Args:
            event: 关闭事件对象
        """
        # 在关闭窗口时保存数据
        self.product_model.save_data()
        event.accept()


def main():
    """主函数"""
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    
    # 设置全局字体
    font = QFont()
    font.setPointSize(10)
    app.setFont(font)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序事件循环
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()