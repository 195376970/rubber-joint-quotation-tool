#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
产品管理界面模块
提供球体和法兰信息的管理功能
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                            QLabel, QLineEdit, QPushButton, QComboBox,
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QMessageBox, QFileDialog, QGroupBox)
from PyQt5.QtCore import Qt


class ProductManagerWidget(QWidget):
    """产品管理界面类"""
    
    def __init__(self, product_model):
        """
        初始化产品管理界面
        
        Args:
            product_model: 产品数据模型实例
        """
        super().__init__()
        self.product_model = product_model
        self.init_ui()
    
    def init_ui(self):
        """初始化UI界面"""
        # 创建主布局
        main_layout = QVBoxLayout()
        
        # 创建标签页切换器
        tab_widget = QTabWidget()
        
        # 创建球体管理和法兰管理标签页
        sphere_tab = self.create_sphere_tab()
        flange_tab = self.create_flange_tab()
        
        # 添加标签页
        tab_widget.addTab(sphere_tab, "球体管理")
        tab_widget.addTab(flange_tab, "法兰管理")
        
        # 创建数据导入导出控件
        import_export_group = self.create_import_export_group()
        
        # 添加到主布局
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(import_export_group)
        
        # 设置布局
        self.setLayout(main_layout)
    
    def create_sphere_tab(self):
        """创建球体管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 添加球体种类区域
        type_group = QGroupBox("添加球体种类")
        type_layout = QHBoxLayout()
        
        type_label = QLabel("种类名称:")
        self.sphere_type_input = QLineEdit()
        add_type_btn = QPushButton("添加")
        add_type_btn.clicked.connect(self.add_sphere_type)
        
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.sphere_type_input)
        type_layout.addWidget(add_type_btn)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # 添加球体型号区域
        model_group = QGroupBox("添加球体型号")
        model_layout = QHBoxLayout()
        
        type_select_label = QLabel("选择种类:")
        self.sphere_type_combo = QComboBox()
        self.update_sphere_type_combo()
        
        model_label = QLabel("型号:")
        self.sphere_model_input = QLineEdit()
        
        price_label = QLabel("价格:")
        self.sphere_price_input = QLineEdit()
        self.sphere_price_input.setPlaceholderText("0.00")
        
        add_model_btn = QPushButton("添加")
        add_model_btn.clicked.connect(self.add_sphere_model)
        
        model_layout.addWidget(type_select_label)
        model_layout.addWidget(self.sphere_type_combo)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.sphere_model_input)
        model_layout.addWidget(price_label)
        model_layout.addWidget(self.sphere_price_input)
        model_layout.addWidget(add_model_btn)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # 球体信息表格
        table_group = QGroupBox("球体信息列表")
        table_layout = QVBoxLayout()
        
        self.sphere_table = QTableWidget(0, 4)
        self.sphere_table.setHorizontalHeaderLabels(["种类", "型号", "价格", "操作"])
        self.sphere_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        table_layout.addWidget(self.sphere_table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        # 更新表格数据
        self.update_sphere_table()
        
        tab.setLayout(layout)
        return tab
    
    def create_flange_tab(self):
        """创建法兰管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 添加法兰种类区域
        type_group = QGroupBox("添加法兰种类")
        type_layout = QHBoxLayout()
        
        type_label = QLabel("种类名称:")
        self.flange_type_input = QLineEdit()
        add_type_btn = QPushButton("添加")
        add_type_btn.clicked.connect(self.add_flange_type)
        
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.flange_type_input)
        type_layout.addWidget(add_type_btn)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # 添加法兰型号区域
        model_group = QGroupBox("添加法兰型号")
        model_layout = QHBoxLayout()
        
        type_select_label = QLabel("选择种类:")
        self.flange_type_combo = QComboBox()
        self.update_flange_type_combo()
        
        model_label = QLabel("型号:")
        self.flange_model_input = QLineEdit()
        
        price_label = QLabel("价格:")
        self.flange_price_input = QLineEdit()
        self.flange_price_input.setPlaceholderText("0.00")
        
        add_model_btn = QPushButton("添加")
        add_model_btn.clicked.connect(self.add_flange_model)
        
        model_layout.addWidget(type_select_label)
        model_layout.addWidget(self.flange_type_combo)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.flange_model_input)
        model_layout.addWidget(price_label)
        model_layout.addWidget(self.flange_price_input)
        model_layout.addWidget(add_model_btn)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # 法兰信息表格
        table_group = QGroupBox("法兰信息列表")
        table_layout = QVBoxLayout()
        
        self.flange_table = QTableWidget(0, 4)
        self.flange_table.setHorizontalHeaderLabels(["种类", "型号", "价格", "操作"])
        self.flange_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        table_layout.addWidget(self.flange_table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        # 更新表格数据
        self.update_flange_table()
        
        tab.setLayout(layout)
        return tab
    
    def create_import_export_group(self):
        """创建数据导入导出控件组"""
        group = QGroupBox("数据导入导出")
        layout = QHBoxLayout()
        
        export_btn = QPushButton("导出产品数据")
        export_btn.clicked.connect(self.export_data)
        
        import_btn = QPushButton("导入产品数据")
        import_btn.clicked.connect(self.import_data)
        
        layout.addWidget(export_btn)
        layout.addWidget(import_btn)
        
        group.setLayout(layout)
        return group
    
    def update_sphere_type_combo(self):
        """更新球体种类下拉框"""
        self.sphere_type_combo.clear()
        self.sphere_type_combo.addItems(self.product_model.sphere_types)
    
    def update_flange_type_combo(self):
        """更新法兰种类下拉框"""
        self.flange_type_combo.clear()
        self.flange_type_combo.addItems(self.product_model.flange_types)
    
    def update_sphere_table(self):
        """更新球体信息表格"""
        self.sphere_table.setRowCount(0)
        
        row = 0
        for sphere_type in self.product_model.sphere_types:
            if sphere_type in self.product_model.sphere_models:
                for model_info in self.product_model.sphere_models[sphere_type]:
                    self.sphere_table.insertRow(row)
                    
                    # 添加表格项
                    type_item = QTableWidgetItem(sphere_type)
                    model_item = QTableWidgetItem(model_info["model"])
                    price_item = QTableWidgetItem(f"{model_info['price']:.2f}")
                    
                    self.sphere_table.setItem(row, 0, type_item)
                    self.sphere_table.setItem(row, 1, model_item)
                    self.sphere_table.setItem(row, 2, price_item)
                    
                    # 添加删除按钮
                    delete_btn = QPushButton("删除")
                    delete_btn.clicked.connect(lambda checked, t=sphere_type, m=model_info["model"]: self.delete_sphere_model(t, m))
                    
                    self.sphere_table.setCellWidget(row, 3, delete_btn)
                    
                    row += 1
    
    def update_flange_table(self):
        """更新法兰信息表格"""
        self.flange_table.setRowCount(0)
        
        row = 0
        for flange_type in self.product_model.flange_types:
            if flange_type in self.product_model.flange_models:
                for model_info in self.product_model.flange_models[flange_type]:
                    self.flange_table.insertRow(row)
                    
                    # 添加表格项
                    type_item = QTableWidgetItem(flange_type)
                    model_item = QTableWidgetItem(model_info["model"])
                    price_item = QTableWidgetItem(f"{model_info['price']:.2f}")
                    
                    self.flange_table.setItem(row, 0, type_item)
                    self.flange_table.setItem(row, 1, model_item)
                    self.flange_table.setItem(row, 2, price_item)
                    
                    # 添加删除按钮
                    delete_btn = QPushButton("删除")
                    delete_btn.clicked.connect(lambda checked, t=flange_type, m=model_info["model"]: self.delete_flange_model(t, m))
                    
                    self.flange_table.setCellWidget(row, 3, delete_btn)
                    
                    row += 1
    
    def add_sphere_type(self):
        """添加球体种类"""
        sphere_type = self.sphere_type_input.text().strip()
        
        if not sphere_type:
            QMessageBox.warning(self, "警告", "种类名称不能为空")
            return
        
        if self.product_model.add_sphere_type(sphere_type):
            self.sphere_type_input.clear()
            self.update_sphere_type_combo()
            QMessageBox.information(self, "成功", f"已添加球体种类: {sphere_type}")
        else:
            QMessageBox.warning(self, "警告", f"球体种类 '{sphere_type}' 已存在")
    
    def add_sphere_model(self):
        """添加球体型号"""
        # 检查是否有球体种类
        if self.sphere_type_combo.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加球体种类")
            return
        
        sphere_type = self.sphere_type_combo.currentText()
        model = self.sphere_model_input.text().strip()
        price_text = self.sphere_price_input.text().strip()
        
        # 验证输入
        if not model:
            QMessageBox.warning(self, "警告", "型号不能为空")
            return
        
        try:
            price = float(price_text) if price_text else 0.0
        except ValueError:
            QMessageBox.warning(self, "警告", "价格必须是有效的数字")
            return
        
        # 添加球体型号
        if self.product_model.add_sphere_model(sphere_type, model, price):
            self.sphere_model_input.clear()
            self.sphere_price_input.clear()
            self.update_sphere_table()
            QMessageBox.information(self, "成功", f"已添加球体型号: {model}")
        else:
            QMessageBox.warning(self, "警告", f"球体型号 '{model}' 已存在于种类 '{sphere_type}' 中")
    
    def delete_sphere_model(self, sphere_type, model):
        """删除球体型号"""
        reply = QMessageBox.question(self, "确认删除", 
                                     f"确定要删除球体种类 '{sphere_type}' 中的型号 '{model}' 吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.product_model.delete_sphere_model(sphere_type, model):
                self.update_sphere_table()
                QMessageBox.information(self, "成功", "已删除球体型号")
            else:
                QMessageBox.warning(self, "警告", "删除球体型号失败")
    
    def add_flange_type(self):
        """添加法兰种类"""
        flange_type = self.flange_type_input.text().strip()
        
        if not flange_type:
            QMessageBox.warning(self, "警告", "种类名称不能为空")
            return
        
        if self.product_model.add_flange_type(flange_type):
            self.flange_type_input.clear()
            self.update_flange_type_combo()
            QMessageBox.information(self, "成功", f"已添加法兰种类: {flange_type}")
        else:
            QMessageBox.warning(self, "警告", f"法兰种类 '{flange_type}' 已存在")
    
    def add_flange_model(self):
        """添加法兰型号"""
        # 检查是否有法兰种类
        if self.flange_type_combo.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加法兰种类")
            return
        
        flange_type = self.flange_type_combo.currentText()
        model = self.flange_model_input.text().strip()
        price_text = self.flange_price_input.text().strip()
        
        # 验证输入
        if not model:
            QMessageBox.warning(self, "警告", "型号不能为空")
            return
        
        try:
            price = float(price_text) if price_text else 0.0
        except ValueError:
            QMessageBox.warning(self, "警告", "价格必须是有效的数字")
            return
        
        # 添加法兰型号
        if self.product_model.add_flange_model(flange_type, model, price):
            self.flange_model_input.clear()
            self.flange_price_input.clear()
            self.update_flange_table()
            QMessageBox.information(self, "成功", f"已添加法兰型号: {model}")
        else:
            QMessageBox.warning(self, "警告", f"法兰型号 '{model}' 已存在于种类 '{flange_type}' 中")
    
    def delete_flange_model(self, flange_type, model):
        """删除法兰型号"""
        reply = QMessageBox.question(self, "确认删除", 
                                     f"确定要删除法兰种类 '{flange_type}' 中的型号 '{model}' 吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.product_model.delete_flange_model(flange_type, model):
                self.update_flange_table()
                QMessageBox.information(self, "成功", "已删除法兰型号")
            else:
                QMessageBox.warning(self, "警告", "删除法兰型号失败")
    
    def export_data(self):
        """导出产品数据"""
        file_path, _ = QFileDialog.getSaveFileName(self, "导出产品数据", "", "JSON文件 (*.json)")
        
        if file_path:
            if not file_path.endswith(".json"):
                file_path += ".json"
            
            if self.product_model.export_data(file_path):
                QMessageBox.information(self, "成功", f"产品数据已导出到 {file_path}")
            else:
                QMessageBox.warning(self, "警告", "导出产品数据失败")
    
    def import_data(self):
        """导入产品数据"""
        file_path, _ = QFileDialog.getOpenFileName(self, "导入产品数据", "", "JSON文件 (*.json)")
        
        if file_path:
            reply = QMessageBox.question(self, "确认导入", 
                                     "导入数据将覆盖当前所有产品信息，确定要继续吗？",
                                     QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                if self.product_model.import_data(file_path):
                    # 更新UI
                    self.update_sphere_type_combo()
                    self.update_flange_type_combo()
                    self.update_sphere_table()
                    self.update_flange_table()
                    
                    QMessageBox.information(self, "成功", "产品数据导入成功")
                else:
                    QMessageBox.warning(self, "警告", "导入产品数据失败，请检查文件格式是否正确")