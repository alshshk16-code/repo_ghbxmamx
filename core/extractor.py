# -*- coding: utf-8 -*-
"""
وحدة المستخرج
تستخرج معلومات الإعداد ونقاط النهاية الإضافية
"""

import re
import json
from utils import logger

class DataExtractor:
    """يستخرج كائنات الإعداد ونقاط النهاية من المحتوى"""
    
    def __init__(self, content):
        """
        تهيئة المستخرج
        
        المعاملات:
            content (str): المحتوى المراد الاستخراج منه
        """
        self.content = content
    
    def extract_stripe_config(self):
        """
        استخراج إعدادات Stripe الخاصة
        
        المخرجات:
            dict: إعدادات Stripe
        """
        config = {
            'publishable_key': None,
            'api_version': None,
            'locale': 'auto',
            'elements_options': {}
        }
        
        # استخراج المفتاح العام
        pk_pattern = r'(pk_(?:test|live)_[a-zA-Z0-9]{24,})'
        pk_matches = re.findall(pk_pattern, self.content)
        if pk_matches:
            config['publishable_key'] = pk_matches[0]
        
        # استخراج إصدار API
        version_pattern = r'["\']apiVersion["\']:\s*["\']([0-9-]+)["\']'
        version_matches = re.findall(version_pattern, self.content)
        if version_matches:
            config['api_version'] = version_matches[0]
        
        # استخراج اللغة
        locale_pattern = r'["\']locale["\']:\s*["\']([a-z]{2}(?:_[A-Z]{2})?)["\']'
        locale_matches = re.findall(locale_pattern, self.content)
        if locale_matches:
            config['locale'] = locale_matches[0]
        
        return config
    
    def extract_braintree_config(self):
        """
        استخراج إعدادات Braintree الخاصة
        
        المخرجات:
            dict: إعدادات Braintree
        """
        config = {
            'authorization': None,
            'client_token': None,
            'merchant_id': None
        }
        
        # استخراج رمز التفويض
        auth_pattern = r'authorization["\']?\s*:\s*["\']([a-zA-Z0-9_-]{20,})["\']'
        auth_matches = re.findall(auth_pattern, self.content)
        if auth_matches:
            config['authorization'] = auth_matches[0]
        
        # استخراج نقطة نهاية رمز العميل
        token_pattern = r'client_token["\']?\s*:\s*["\']([^"\']+)["\']'
        token_matches = re.findall(token_pattern, self.content)
        if token_matches:
            config['client_token'] = token_matches[0]
        
        return config
    
    def extract_api_endpoints(self):
        """
        استخراج روابط نقاط نهاية API
        
        المخرجات:
            list: قائمة نقاط نهاية API
        """
        endpoints = []
        
        # أنماط نقاط النهاية الشائعة
        patterns = [
            r'https?://[a-zA-Z0-9.-]+/api/[a-zA-Z0-9/_-]+',
            r'["\']/(api|payment|checkout)/[a-zA-Z0-9/_-]+["\']',
            r'endpoint["\']?\s*:\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, self.content)
            endpoints.extend(matches)
        
        # إزالة التكرارات والتنظيف
        endpoints = list(set(endpoints))
        endpoints = [e.strip('"\'') for e in endpoints]
        
        return endpoints
    
    def extract_form_data(self):
        """
        استخراج أسماء حقول نموذج الدفع
        
        المخرجات:
            dict: معلومات حقول النموذج
        """
        fields = {
            'card_number': [],
            'expiry': [],
            'cvc': [],
            'cardholder': []
        }
        
        # أنماط حقل رقم البطاقة
        card_patterns = [
            r'name=["\']([^"\']*(?:card|number)[^"\']*)["\']',
            r'id=["\']([^"\']*(?:card|number)[^"\']*)["\']'
        ]
        
        for pattern in card_patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            fields['card_number'].extend(matches)
        
        # أنماط حقل تاريخ الانتهاء
        expiry_patterns = [
            r'name=["\']([^"\']*(?:exp|expiry|expiration)[^"\']*)["\']',
            r'id=["\']([^"\']*(?:exp|expiry|expiration)[^"\']*)["\']'
        ]
        
        for pattern in expiry_patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            fields['expiry'].extend(matches)
        
        # أنماط حقل CVC
        cvc_patterns = [
            r'name=["\']([^"\']*(?:cvc|cvv|security)[^"\']*)["\']',
            r'id=["\']([^"\']*(?:cvc|cvv|security)[^"\']*)["\']'
        ]
        
        for pattern in cvc_patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            fields['cvc'].extend(matches)
        
        # إزالة التكرارات
        for key in fields:
            fields[key] = list(set(fields[key]))
        
        return fields
    
    def extract_currency_info(self):
        """
        استخراج معلومات العملة
        
        المخرجات:
            list: قائمة العملات المستخدمة
        """
        currencies = []
        
        # رموز العملات الشائعة
        currency_pattern = r'["\'](?:currency|curr)["\']?\s*:\s*["\']([A-Z]{3})["\']'
        matches = re.findall(currency_pattern, self.content, re.IGNORECASE)
        currencies.extend(matches)
        
        # رموز العملات
        symbol_map = {
            '$': 'USD',
            '€': 'EUR',
            '£': 'GBP',
            '¥': 'JPY'
        }
        
        for symbol, code in symbol_map.items():
            if symbol in self.content:
                currencies.append(code)
        
        return list(set(currencies))
    
    def extract_all(self, gateway_name=None):
        """
        استخراج جميع المعلومات المتاحة
        
        المعاملات:
            gateway_name (str): بوابة محددة للاستخراج منها
            
        المخرجات:
            dict: جميع المعلومات المستخرجة
        """
        logger.info("استخراج الإعدادات الإضافية...")
        
        result = {
            'endpoints': self.extract_api_endpoints(),
            'form_fields': self.extract_form_data(),
            'currencies': self.extract_currency_info()
        }
        
        if gateway_name == 'stripe':
            result['stripe_config'] = self.extract_stripe_config()
            logger.debug(f"تم استخراج إعدادات Stripe: {result['stripe_config']}")
        elif gateway_name == 'braintree':
            result['braintree_config'] = self.extract_braintree_config()
            logger.debug(f"تم استخراج إعدادات Braintree: {result['braintree_config']}")
        
        logger.success("اكتمل استخراج الإعدادات")
        return result
