#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
报价计算界面模块
提供接头配置和报价单管理功能
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QComboBox, QTableWidget,
                            QTableWidgetItem, QHeaderView, QMessageBox,
                            QFileDialog, QGroupBox, QSpinBox, QDoubleSpinBox,
                            QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class QuotationCalculatorWidget(QWidget):
    """报价计算界面类"""
    
    def __init__(self, product_model, quotation_model):
        """
        初始化报价计算界面
        
        Args:
            product_model: 产品数据模型实例
            quotation_model: 报价单数据模型实例
        """
        super().__init__()
        self.product_model = product_model
        self.quotation_model = quotation_model
        self.init_ui()
    
    def init_ui(self):
        """初始化UI界面"""
        # 创建主布局
        main_layout = QVBoxLayout()
        
        # 创建接头配置区域
        config_group = self.create_config_group()
        
        # 创建报价单显示区域
        quotation_group = self.create_quotation_group()
        
        # 创建报价单操作区域
        operation_group = self.create_operation_group()
        
        # 添加到主布局
        main_layout.addWidget(config_group)
        main_layout.addWidget(quotation_group)
        main_layout.addWidget(operation_group)
        
        # 设置布局
        self.setLayout(main_layout)
    
    def create_config_group(self):
        """创建接头配置区域"""
        group = QGroupBox("接头配置")
        layout = QVBoxLayout()
        
        # 球体选择区域
        sphere_form = QFormLayout()
        
        # 球体种类选择
        self.sphere_type_combo = QComboBox()
        self.sphere_type_combo.currentIndexChanged.connect(self.update_sphere_model_combo)
        sphere_form.addRow("球体种类:", self.sphere_type_combo)
        
        # 球体型号选择
        self.sphere_model_combo = QComboBox()
        sphere_form.addRow("球体型号:", self.sphere_model_combo)
        
        # 法兰选择区域
        flange_form = QFormLayout()
        
        # 法兰种类选择
        self.flange_type_combo = QComboBox()
        self.flange_type_combo.currentIndexChanged.connect(self.update_flange_model_combo)
        flange_form.addRow("法兰种类:", self.flange_type_combo)
        
        # 法兰型号选择
        self.flange_model_combo = QComboBox()
        flange_form.addRow("法兰型号:", self.flange_model_combo)
        
        # 法兰数量选择
        self.flange_quantity_spin = QSpinBox()
        self.flange_quantity_spin.setRange(1, 4)
        self.flange_quantity_spin.setValue(2)
        flange_form.addRow("法兰数量:", self.flange_quantity_spin)
        
        # 上部分布局
        upper_layout = QHBoxLayout()
        upper_layout.addLayout(sphere_form)
        upper_layout.addLayout(flange_form)
        
        # 添加上部分布局
        layout.addLayout(upper_layout)
        
        # 接头数量和价格计算区域
        lower_layout = QHBoxLayout()
        
        # 接头数量输入框
        joint_quantity_layout = QFormLayout()
        self.joint_quantity_spin = QSpinBox()
        self.joint_quantity_spin.setRange(1, 1000)
        self.joint_quantity_spin.setValue(1)
        joint_quantity_layout.addRow("接头数量:", self.joint_quantity_spin)
        
        # 当前单价显示
        price_layout = QFormLayout()
        self.current_price_label = QLabel("0.00")
        self.current_price_label.setFont(QFont("Arial", 12, QFont.Bold))
        price_layout.addRow("当前接头单价:", self.current_price_label)
        
        # 添加按钮区域
        button_layout = QVBoxLayout()
        
        # 计算按钮
        calculate_btn = QPushButton("计算当前接头价格")
        calculate_btn.clicked.connect(self.calculate_current_price)
        
        # 添加到报价单按钮
        add_to_quotation_btn = QPushButton("添加到报价单")
        add_to_quotation_btn.clicked.connect(self.add_to_quotation)
        
        button_layout.addWidget(calculate_btn)
        button_layout.addWidget(add_to_quotation_btn)
        
        # 添加到下部分布局
        lower_layout.addLayout(joint_quantity_layout)
        lower_layout.addLayout(price_layout)
        lower_layout.addLayout(button_layout)
        
        # 添加下部分布局
        layout.addLayout(lower_layout)
        
        # 设置组框布局
        group.setLayout(layout)
        
        # 更新下拉框
        self.update_type_combos()
        
        return group
    
    def create_quotation_group(self):
        """创建报价单显示区域"""
        group = QGroupBox("报价单明细")
        layout = QVBoxLayout()
        
        # 报价单表格
        self.quotation_table = QTableWidget(0, 8)
        headers = ["序号", "球体信息", "法兰信息", "法兰数量", "接头数量", "单价(元)", "小计(元)", "操作"]
        self.quotation_table.setHorizontalHeaderLabels(headers)
        self.quotation_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 总价显示
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        
        total_label = QLabel("总价:")
        self.total_price_label = QLabel("0.00")
        self.total_price_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_price_label)
        
        # 添加到布局
        layout.addWidget(self.quotation_table)
        layout.addLayout(total_layout)
        
        # 设置组框布局
        group.setLayout(layout)
        
        return group
    
    def create_operation_group(self):
        """创建报价单操作区域"""
        group = QGroupBox("报价单操作")
        layout = QHBoxLayout()
        
        # 清空报价单按钮
        clear_btn = QPushButton("清空报价单")
        clear_btn.clicked.connect(self.clear_quotation)
        
        # 生成报价单按钮
        generate_btn = QPushButton("生成报价单")
        generate_btn.clicked.connect(self.generate_quotation)
        
        # 保存报价单数据按钮
        save_btn = QPushButton("保存报价单数据")
        save_btn.clicked.connect(self.save_quotation_data)
        
        # 加载报价单数据按钮
        load_btn = QPushButton("加载报价单数据")
        load_btn.clicked.connect(self.load_quotation_data)
        
        # 添加到布局
        layout.addWidget(clear_btn)
        layout.addWidget(generate_btn)
        layout.addWidget(save_btn)
        layout.addWidget(load_btn)
        
        # 设置组框布局
        group.setLayout(layout)
        
        return group
    
    def update_type_combos(self):
        """更新所有类型选择框"""
        # 更新球体种类下拉框
        self.sphere_type_combo.clear()
        self.sphere_type_combo.addItems(self.product_model.sphere_types)
        
        # 更新法兰种类下拉框
        self.flange_type_combo.clear()
        self.flange_type_combo.addItems(self.product_model.flange_types)
        
        # 更新对应的型号下拉框
        self.update_sphere_model_combo()
        self.update_flange_model_combo()
    
    def update_sphere_model_combo(self):
        """根据选择的球体种类更新型号下拉框"""
        self.sphere_model_combo.clear()
        
        sphere_type = self.sphere_type_combo.currentText()
        if sphere_type:
            models = self.product_model.get_sphere_models_by_type(sphere_type)
            self.sphere_model_combo.addItems(models)
    
    def update_flange_model_combo(self):
        """根据选择的法兰种类更新型号下拉框"""
        self.flange_model_combo.clear()
        
        flange_type = self.flange_type_combo.currentText()
        if flange_type:
            models = self.product_model.get_flange_models_by_type(flange_type)
            self.flange_model_combo.addItems(models)
    
    def calculate_current_price(self):
        """计算当前配置的接头单价"""
        # 检查是否已选择所有必要的项目
        if (self.sphere_type_combo.count() == 0 or
            self.sphere_model_combo.count() == 0 or
            self.flange_type_combo.count() == 0 or
            self.flange_model_combo.count() == 0):
            QMessageBox.warning(self, "警告", "请确保已选择球体和法兰的种类及型号")
            return
        
        # 获取选择的配置
        sphere_type = self.sphere_type_combo.currentText()
        sphere_model = self.sphere_model_combo.currentText()
        flange_type = self.flange_type_combo.currentText()
        flange_model = self.flange_model_combo.currentText()
        flange_quantity = self.flange_quantity_spin.value()
        
        # 计算接头单价
        joint_price = self.quotation_model.calculate_joint_price(
            sphere_type, sphere_model, flange_type, flange_model, flange_quantity
        )
        
        # 更新显示
        self.current_price_label.setText(f"{joint_price:.2f}")
    
    def add_to_quotation(self):
        """将当前配置添加到报价单"""
        # 检查是否已选择所有必要的项目
        if (self.sphere_type_combo.count() == 0 or
            self.sphere_model_combo.count() == 0 or
            self.flange_type_combo.count() == 0 or
            self.flange_model_combo.count() == 0):
            QMessageBox.warning(self, "警告", "请确保已选择球体和法兰的种类及型号")
            return
        
        # 获取选择的配置
        sphere_type = self.sphere_type_combo.currentText()
        sphere_model = self.sphere_model_combo.currentText()
        flange_type = self.flange_type_combo.currentText()
        flange_model = self.flange_model_combo.currentText()
        flange_quantity = self.flange_quantity_spin.value()
        joint_quantity = self.joint_quantity_spin.value()
        
        # 添加到报价单
        item_total = self.quotation_model.add_item(
            sphere_type, sphere_model, flange_type, flange_model, flange_quantity, joint_quantity
        )
        
        # 更新报价单显示
        self.update_quotation_table()
        
        # 更新总价显示
        self.total_price_label.setText(f"{self.quotation_model.total_price:.2f}")
        
        QMessageBox.information(self, "成功", f"已添加到报价单，小计: {item_total:.2f}元")
    
    def update_quotation_table(self):
        """更新报价单表格"""
        self.quotation_table.setRowCount(0)
        
        for i, item in enumerate(self.quotation_model.quotation_items):
            self.quotation_table.insertRow(i)
            
            # 序号
            index_item = QTableWidgetItem(str(i + 1))
            
            # 球体信息
            sphere_info = f"{item['sphereType']} - {item['sphereModel']}"
            sphere_item = QTableWidgetItem(sphere_info)
            
            # 法兰信息
            flange_info = f"{item['flangeType']} - {item['flangeModel']}"
            flange_item = QTableWidgetItem(flange_info)
            
            # 法兰数量
            flange_quantity_item = QTableWidgetItem(str(item['flangeQuantity']))
            
            # 接头数量
            joint_quantity_item = QTableWidgetItem(str(item['jointQuantity']))
            
            # 单价
            price_item = QTableWidgetItem(f"{item['jointPrice']:.2f}")
            
            # 小计
            total_item = QTableWidgetItem(f"{item['totalPrice']:.2f}")
            
            # 添加表格项
            self.quotation_table.setItem(i, 0, index_item)
            self.quotation_table.setItem(i, 1, sphere_item)
            self.quotation_table.setItem(i, 2, flange_item)
            self.quotation_table.setItem(i, 3, flange_quantity_item)
            self.quotation_table.setItem(i, 4, joint_quantity_item)
            self.quotation_table.setItem(i, 5, price_item)
            self.quotation_table.setItem(i, 6, total_item)
            
            # 添加删除按钮
            delete_btn = QPushButton("删除")
            delete_btn.clicked.connect(lambda checked, idx=i: self.delete_quotation_item(idx))
            
            self.quotation_table.setCellWidget(i, 7, delete_btn)
        
        # 更新总价显示
        self.total_price_label.setText(f"{self.quotation_model.total_price:.2f}")
    
    def delete_quotation_item(self, index):
        """删除报价单项目"""
        if self.quotation_model.delete_item(index):
            self.update_quotation_table()
        else:
            QMessageBox.warning(self, "警告", "删除报价单项目失败")
    
    def clear_quotation(self):
        """清空报价单"""
        if len(self.quotation_model.quotation_items) == 0:
            return
        
        reply = QMessageBox.question(self, "确认清空", 
                                    "确定要清空整个报价单吗？",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.quotation_model.clear_items()
            self.update_quotation_table()
            QMessageBox.information(self, "成功", "已清空报价单")
    
    def save_quotation_data(self):
        """保存报价单数据"""
        if len(self.quotation_model.quotation_items) == 0:
            QMessageBox.warning(self, "警告", "报价单为空，无法保存")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, "保存报价单数据", "", "JSON文件 (*.json)")
        
        if file_path:
            if not file_path.endswith(".json"):
                file_path += ".json"
            
            if self.quotation_model.save_quotation(file_path):
                QMessageBox.information(self, "成功", f"报价单数据已保存到 {file_path}")
            else:
                QMessageBox.warning(self, "警告", "保存报价单数据失败")
    
    def load_quotation_data(self):
        """加载报价单数据"""
        file_path, _ = QFileDialog.getOpenFileName(self, "加载报价单数据", "", "JSON文件 (*.json)")
        
        if file_path:
            reply = QMessageBox.question(self, "确认加载", 
                                     "加载数据将覆盖当前报价单，确定要继续吗？",
                                     QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                if self.quotation_model.load_quotation(file_path):
                    self.update_quotation_table()
                    QMessageBox.information(self, "成功", "报价单数据加载成功")
                else:
                    QMessageBox.warning(self, "警告", "加载报价单数据失败，请检查文件格式是否正确")
    
    def generate_quotation(self):
        """生成报价单"""
        if len(self.quotation_model.quotation_items) == 0:
            QMessageBox.warning(self, "警告", "报价单为空，无法生成")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, "保存报价单", "", "PDF文件 (*.pdf)")
        
        if file_path:
            if not file_path.endswith(".pdf"):
                file_path += ".pdf"
            
            try:
                self.create_quotation_pdf(file_path)
                QMessageBox.information(self, "成功", f"报价单已生成: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "警告", f"生成报价单失败: {e}")
    
    def create_quotation_pdf(self, file_path):
        """
        创建PDF格式的报价单
        
        Args:
            file_path (str): 保存文件路径
        """
        # 创建PDF文档
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        elements = []
        
        # 获取样式
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        normal_style = styles["Normal"]
        
        # 添加标题
        elements.append(Paragraph("橡胶接头报价单", title_style))
        elements.append(Spacer(1, 20))
        
        # 添加日期
        date_text = f"日期: {datetime.now().strftime('%Y-%m-%d')}"
        elements.append(Paragraph(date_text, normal_style))
        elements.append(Spacer(1, 20))
        
        # 创建表格数据
        table_data = [
            ["序号", "球体信息", "法兰信息", "法兰数量", "接头数量", "单价(元)", "小计(元)"]
        ]
        
        # 添加报价项目
        for i, item in enumerate(self.quotation_model.quotation_items):
            sphere_info = f"{item['sphereType']} - {item['sphereModel']}"
            flange_info = f"{item['flangeType']} - {item['flangeModel']}"
            
            row = [
                str(i + 1),
                sphere_info,
                flange_info,
                str(item['flangeQuantity']),
                str(item['jointQuantity']),
                f"{item['jointPrice']:.2f}",
                f"{item['totalPrice']:.2f}"
            ]
            
            table_data.append(row)
        
        # 添加总计行
        total_row = ["", "", "", "", "", "总计", f"{self.quotation_model.total_price:.2f}"]
        table_data.append(total_row)
        
        # 创建表格
        table = Table(table_data)
        
        # 设置表格样式
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, -1), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -2), 1, colors.black),
            ('GRID', (-2, -1), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ])
        
        table.setStyle(style)
        
        # 添加表格到文档
        elements.append(table)
        
        # 添加备注
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("备注:", normal_style))
        elements.append(Paragraph("1. 价格单位为人民币元。", normal_style))
        elements.append(Paragraph("2. 报价单有效期为30天。", normal_style))
        elements.append(Paragraph("3. 如有疑问，请联系我们。", normal_style))
        
        # 构建PDF
        doc.build(elements)