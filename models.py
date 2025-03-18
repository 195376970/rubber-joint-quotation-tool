#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据模型模块
包含球体、法兰和报价单数据模型的定义
"""

import json
import os
from datetime import datetime


class ProductDataModel:
    """产品数据模型类，管理球体和法兰信息"""
    
    def __init__(self):
        """初始化产品数据模型"""
        # 球体数据结构
        self.sphere_types = []  # 球体种类列表
        self.sphere_models = {}  # 球体型号和价格信息
        
        # 法兰数据结构
        self.flange_types = []  # 法兰种类列表
        self.flange_models = {}  # 法兰型号和价格信息
        
        # 尝试加载保存的数据
        self.load_data()
    
    def add_sphere_type(self, sphere_type):
        """
        添加球体种类
        
        Args:
            sphere_type (str): 球体种类名称
            
        Returns:
            bool: 是否添加成功
        """
        if sphere_type and sphere_type not in self.sphere_types:
            self.sphere_types.append(sphere_type)
            self.sphere_models[sphere_type] = []
            self.save_data()
            return True
        return False
    
    def add_sphere_model(self, sphere_type, model, price):
        """
        添加球体型号
        
        Args:
            sphere_type (str): 球体种类名称
            model (str): 球体型号
            price (float): 球体价格
            
        Returns:
            bool: 是否添加成功
        """
        if sphere_type in self.sphere_types and model:
            # 检查是否已存在相同型号
            for item in self.sphere_models[sphere_type]:
                if item["model"] == model:
                    return False
            
            self.sphere_models[sphere_type].append({
                "model": model,
                "price": float(price)
            })
            self.save_data()
            return True
        return False
    
    def delete_sphere_type(self, sphere_type):
        """
        删除球体种类
        
        Args:
            sphere_type (str): 球体种类名称
            
        Returns:
            bool: 是否删除成功
        """
        if sphere_type in self.sphere_types:
            self.sphere_types.remove(sphere_type)
            if sphere_type in self.sphere_models:
                del self.sphere_models[sphere_type]
            self.save_data()
            return True
        return False
    
    def delete_sphere_model(self, sphere_type, model):
        """
        删除球体型号
        
        Args:
            sphere_type (str): 球体种类名称
            model (str): 球体型号
            
        Returns:
            bool: 是否删除成功
        """
        if sphere_type in self.sphere_models:
            for i, item in enumerate(self.sphere_models[sphere_type]):
                if item["model"] == model:
                    self.sphere_models[sphere_type].pop(i)
                    self.save_data()
                    return True
        return False
    
    def add_flange_type(self, flange_type):
        """
        添加法兰种类
        
        Args:
            flange_type (str): 法兰种类名称
            
        Returns:
            bool: 是否添加成功
        """
        if flange_type and flange_type not in self.flange_types:
            self.flange_types.append(flange_type)
            self.flange_models[flange_type] = []
            self.save_data()
            return True
        return False
    
    def add_flange_model(self, flange_type, model, price):
        """
        添加法兰型号
        
        Args:
            flange_type (str): 法兰种类名称
            model (str): 法兰型号
            price (float): 法兰价格
            
        Returns:
            bool: 是否添加成功
        """
        if flange_type in self.flange_types and model:
            # 检查是否已存在相同型号
            for item in self.flange_models[flange_type]:
                if item["model"] == model:
                    return False
            
            self.flange_models[flange_type].append({
                "model": model,
                "price": float(price)
            })
            self.save_data()
            return True
        return False
    
    def delete_flange_type(self, flange_type):
        """
        删除法兰种类
        
        Args:
            flange_type (str): 法兰种类名称
            
        Returns:
            bool: 是否删除成功
        """
        if flange_type in self.flange_types:
            self.flange_types.remove(flange_type)
            if flange_type in self.flange_models:
                del self.flange_models[flange_type]
            self.save_data()
            return True
        return False
    
    def delete_flange_model(self, flange_type, model):
        """
        删除法兰型号
        
        Args:
            flange_type (str): 法兰种类名称
            model (str): 法兰型号
            
        Returns:
            bool: 是否删除成功
        """
        if flange_type in self.flange_models:
            for i, item in enumerate(self.flange_models[flange_type]):
                if item["model"] == model:
                    self.flange_models[flange_type].pop(i)
                    self.save_data()
                    return True
        return False
    
    def get_sphere_price(self, sphere_type, model):
        """
        获取球体价格
        
        Args:
            sphere_type (str): 球体种类名称
            model (str): 球体型号
            
        Returns:
            float: 球体价格
        """
        if sphere_type in self.sphere_models:
            for item in self.sphere_models[sphere_type]:
                if item["model"] == model:
                    return item["price"]
        return 0.0
    
    def get_flange_price(self, flange_type, model):
        """
        获取法兰价格
        
        Args:
            flange_type (str): 法兰种类名称
            model (str): 法兰型号
            
        Returns:
            float: 法兰价格
        """
        if flange_type in self.flange_models:
            for item in self.flange_models[flange_type]:
                if item["model"] == model:
                    return item["price"]
        return 0.0
    
    def get_sphere_models_by_type(self, sphere_type):
        """
        获取指定种类的球体型号列表
        
        Args:
            sphere_type (str): 球体种类名称
            
        Returns:
            list: 球体型号列表
        """
        if sphere_type in self.sphere_models:
            return [item["model"] for item in self.sphere_models[sphere_type]]
        return []
    
    def get_flange_models_by_type(self, flange_type):
        """
        获取指定种类的法兰型号列表
        
        Args:
            flange_type (str): 法兰种类名称
            
        Returns:
            list: 法兰型号列表
        """
        if flange_type in self.flange_models:
            return [item["model"] for item in self.flange_models[flange_type]]
        return []
    
    def save_data(self):
        """保存产品数据到文件"""
        data = {
            "sphereTypes": self.sphere_types,
            "sphereModels": self.sphere_models,
            "flangeTypes": self.flange_types,
            "flangeModels": self.flange_models,
            "exportDate": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        try:
            # 确保数据目录存在
            if not os.path.exists("data"):
                os.makedirs("data")
            
            # 保存数据到JSON文件
            with open("data/product_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def load_data(self):
        """从文件加载产品数据"""
        try:
            # 检查数据文件是否存在
            if os.path.exists("data/product_data.json"):
                with open("data/product_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 加载数据
                self.sphere_types = data.get("sphereTypes", [])
                self.sphere_models = data.get("sphereModels", {})
                self.flange_types = data.get("flangeTypes", [])
                self.flange_models = data.get("flangeModels", {})
                return True
        except Exception as e:
            print(f"加载数据失败: {e}")
        return False
    
    def export_data(self, file_path):
        """
        导出产品数据到指定文件
        
        Args:
            file_path (str): 导出文件路径
            
        Returns:
            bool: 是否导出成功
        """
        data = {
            "sphereTypes": self.sphere_types,
            "sphereModels": self.sphere_models,
            "flangeTypes": self.flange_types,
            "flangeModels": self.flange_models,
            "exportDate": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"导出数据失败: {e}")
            return False
    
    def import_data(self, file_path):
        """
        从指定文件导入产品数据
        
        Args:
            file_path (str): 导入文件路径
            
        Returns:
            bool: 是否导入成功
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 验证数据格式
            if all(key in data for key in ["sphereTypes", "sphereModels", "flangeTypes", "flangeModels"]):
                self.sphere_types = data["sphereTypes"]
                self.sphere_models = data["sphereModels"]
                self.flange_types = data["flangeTypes"]
                self.flange_models = data["flangeModels"]
                self.save_data()
                return True
        except Exception as e:
            print(f"导入数据失败: {e}")
        return False


class QuotationModel:
    """报价单数据模型类，管理报价单信息"""
    
    def __init__(self, product_model):
        """
        初始化报价单数据模型
        
        Args:
            product_model (ProductDataModel): 产品数据模型实例
        """
        self.product_model = product_model
        self.quotation_items = []  # 报价单项目列表
        self.total_price = 0.0  # 总价
    
    def add_item(self, sphere_type, sphere_model, flange_type, flange_model, flange_quantity, joint_quantity):
        """
        添加报价项目
        
        Args:
            sphere_type (str): 球体种类
            sphere_model (str): 球体型号
            flange_type (str): 法兰种类
            flange_model (str): 法兰型号
            flange_quantity (int): 法兰数量
            joint_quantity (int): 接头数量
            
        Returns:
            float: 项目小计价格
        """
        # 获取价格信息
        sphere_price = self.product_model.get_sphere_price(sphere_type, sphere_model)
        flange_price = self.product_model.get_flange_price(flange_type, flange_model)
        
        # 计算单个接头价格
        joint_price = sphere_price + flange_price * flange_quantity
        
        # 计算小计
        item_total = joint_price * joint_quantity
        
        # 添加到报价单
        self.quotation_items.append({
            "sphereType": sphere_type,
            "sphereModel": sphere_model,
            "flangeType": flange_type,
            "flangeModel": flange_model,
            "flangeQuantity": flange_quantity,
            "jointQuantity": joint_quantity,
            "spherePrice": sphere_price,
            "flangePrice": flange_price,
            "jointPrice": joint_price,
            "totalPrice": item_total
        })
        
        # 更新总价
        self.update_total_price()
        
        return item_total
    
    def delete_item(self, index):
        """
        删除报价项目
        
        Args:
            index (int): 项目索引
            
        Returns:
            bool: 是否删除成功
        """
        if 0 <= index < len(self.quotation_items):
            self.quotation_items.pop(index)
            self.update_total_price()
            return True
        return False
    
    def clear_items(self):
        """清空报价单"""
        self.quotation_items = []
        self.total_price = 0.0
    
    def update_total_price(self):
        """更新报价单总价"""
        self.total_price = sum(item["totalPrice"] for item in self.quotation_items)
    
    def calculate_joint_price(self, sphere_type, sphere_model, flange_type, flange_model, flange_quantity):
        """
        计算单个接头价格
        
        Args:
            sphere_type (str): 球体种类
            sphere_model (str): 球体型号
            flange_type (str): 法兰种类
            flange_model (str): 法兰型号
            flange_quantity (int): 法兰数量
            
        Returns:
            float: 接头单价
        """
        sphere_price = self.product_model.get_sphere_price(sphere_type, sphere_model)
        flange_price = self.product_model.get_flange_price(flange_type, flange_model)
        
        return sphere_price + flange_price * flange_quantity
    
    def save_quotation(self, file_path):
        """
        保存报价单数据到文件
        
        Args:
            file_path (str): 保存文件路径
            
        Returns:
            bool: 是否保存成功
        """
        data = {
            "quotationItems": self.quotation_items,
            "totalPrice": self.total_price,
            "saveDate": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存报价单失败: {e}")
            return False
    
    def load_quotation(self, file_path):
        """
        从文件加载报价单数据
        
        Args:
            file_path (str): 加载文件路径
            
        Returns:
            bool: 是否加载成功
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 验证数据格式
            if "quotationItems" in data:
                self.quotation_items = data["quotationItems"]
                self.update_total_price()
                return True
        except Exception as e:
            print(f"加载报价单失败: {e}")
        return False